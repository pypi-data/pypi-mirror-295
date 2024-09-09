from pyspark.sql import SparkSession
from delta import *
import getpass
import pandas as pd
import shutil
import duckdb

from .helpers import *
from .config import *
from .auth import *

from .sources.mssql import mssql
from .sources.parquet import parquet
from .sources.csv import csv
from .sources.delta import delta


from .quality.checks import check

class spark(SparkSession):
    def __init__(self, spark_memory, spark_cpu_cores):
        self.spark_cpu_cores = spark_cpu_cores
        self.spark_memory = spark_memory
        self.spark_session = self.__create_spark_session()


    def __create_spark_session(self):
        builder = super().builder.master(f'local[{self.spark_cpu_cores}]') \
            .config('spark.driver.extraClassPath', jar_files) \
            .config('spark.executor.extraClassPath', jar_files) \
            .config('spark.sql.extensions', 'io.delta.sql.DeltaSparkSessionExtension') \
            .config('spark.sql.catalog.spark_catalog', 'org.apache.spark.sql.delta.catalog.DeltaCatalog') \
            .config('spark.sql.warehouse.dir', spark_warehouse) \
            .config('spark.driver.memory', self.spark_memory) \
            .config('spark.driver.maxResultSize', self.spark_memory) \
            .config('spark.sql.repl.eagerEval.enabled', True) \
            .config('spark.databricks.delta.schema.autoMerge.enabled', True) \
            .config('spark.databricks.delta.autoCompact.enabled', True)
        return builder.getOrCreate()

class app:
    def __init__(self, username: str, password: str = None, spark_memory: str = "10g", spark_cpu_cores = "8"):
        self.spark_cpu_cores = spark_cpu_cores
        self.spark_memory = spark_memory
        self.username = username
        if not password:
            self.password = getpass.getpass('Please enter your password: ')
        else:
            self.password = password
        self.auth = auth(self.username, self.password)
        if not self.auth.login():
            print('The username and/or password is incorrect. Please try again.')
            return None
        self.spark = spark(self.spark_memory, self.spark_cpu_cores).spark_session
        self.sources = []

    
    # load metastore to the spark session of the app
    def load(self):
        if not self.auth.login():
            print('The username and/or password is incorrect. Please try again.')
            return None
        rows = self.auth.get_access_level()
        for row in rows:
            try:
                self.spark.sql(row.script)
            except:
                pass

    
    # perform sql commands
    def sql(self, script):
        if not self.auth.login():
            print('The username and/or password is incorrect. Please try again.')
            return None
        return self.__sql(script)


    def table_query(self, script: str):
        postgres_conn = get_metastore_con()
        engine = create_engine(postgres_conn, isolation_level='AUTOCOMMIT')
        with engine.connect() as conn:
            sql = f'''
                select name, "location" from 
                delta_objects dlo inner join delta_objects_users dou on dlo.id = dou.object_id
                inner join delta_users du on du.id = dou.user_id 
                where "type" = 'table' and du.username = '{self.username}'
            '''
            output = conn.execute(text(sql)).fetchall()
        duckdb.sql('load delta')
        script = normalize_script(script)
        for item in output:
            script = script.replace(item[0], f'delta_scan("{item[1]}")')
        return duckdb.sql(script).df()
        
    
    def terminate(self):
        self.spark.stop()
        # logout


    def add_source(self, params):
        if params.get('source_type').strip().lower() == 'mssql':
            x = mssql(
                app = self,
                source_name = params.get('source_name'),
                server = params.get('server'),
                database = params.get('database'),
                db_username = params.get('db_username'),
                db_password = params.get('db_password'),
                port = params.get('port')
            )
            self.sources.append(x)
            return x
            
        elif params.get('source_type').strip().lower() == 'parquet':
            x = parquet(
                    app = self,
                    source_name = params.get('source_name'),
                    file_path = params.get('file_path')
            )
            self.sources.append(x)
            return x
            
        elif params.get('source_type').strip().lower() == 'csv':
            x = csv(
                    app = self,
                    source_name = params.get('source_name'),
                    file_path = params.get('file_path')
            )
            self.sources.append(x)
            return x

        elif params.get('source_type').strip().lower() == 'delta':
            x = delta(
                    app = self,
                    source_name = params.get('source_name')
            )
            self.sources.append(x)
            return x


    # get a source by part of its source_name
    def get_source_by_name(self, name: str):
        return [{'source_name':source.source_name, 'source_instance':source} for source in self.sources if name.strip().lower() in source.source_name.strip().lower()]

    
    # get the access level for the current user
    def get_access_level_report(self):
        postgres_conn = get_metastore_con()
        engine = create_engine(postgres_conn, isolation_level='AUTOCOMMIT')
        sql = f'''select 
            name, 
            "type", 
            "location",
            case 
            	when dou.access_level = 'r' then 'Read'
            	when dou.access_level = 'w' then 'Write'
            	when dou.access_level = 'c' then 'Change'
            	when dou.access_level = 'rw' then 'Read - Write'
            	when dou.access_level = 'rc' then 'Read - Change'
            	when dou.access_level = 'wc' then 'Write - Change'
            	when dou.access_level = 'rwc' then 'Read - Write - Change'
                else 'No Permission'
            end as access_level
        from delta_objects dlo inner join delta_objects_users dou on dou.object_id = dlo.id
        inner join delta_users du on du.id = dou.user_id
        where du.username = '{self.username}'
        '''
        return pd.read_sql(sql, engine)
            
            
    def set_access_level(self, username: str, object_name: str, access_level: str):
        postgres_conn = get_metastore_con()
        engine = create_engine(postgres_conn, isolation_level='AUTOCOMMIT')
        current_user = self.username
        
        with engine.connect() as conn:
            sql = f''' select id from delta_users du where username = '{current_user}' '''
            current_user_id = conn.execute(text(sql)).fetchone()[0]
    
        with engine.connect() as conn:
            sql = f''' select id from delta_objects where name = '{object_name}' '''
            object_id = conn.execute(text(sql)).fetchone()[0]
    
        with engine.connect() as conn:
            sql = f''' select access_level from delta_objects_users where user_id = {current_user_id} and object_id = {object_id}'''
            current_access_level = conn.execute(text(sql)).fetchone()[0]
    
        if 'c' not in current_access_level:
            print('''You don't have enough permission to give access of this object to the user.''')
            return
        
        with engine.connect() as conn:
            sql = f''' select id from delta_users du where username = '{username}' '''
            user_id = conn.execute(text(sql)).fetchone()[0]
    
    
        with engine.connect() as conn:
            sql = f''' select id from delta_objects_users where user_id = {user_id} and object_id = {object_id} '''
            row = conn.execute(text(sql)).fetchone()
    
            if not row:
                sql = f''' insert into delta_objects_users (user_id, object_id, access_level) values ({user_id}, {object_id}, '{access_level}') '''
                conn.execute(text(sql))
            else:
                sql = f''' update delta_objects_users set access_level = '{access_level}' where user_id = {user_id} and object_id = {object_id} '''
                conn.execute(text(sql))


    def drop_object(self, name: str):
        postgres_conn = get_metastore_con()
        engine = create_engine(postgres_conn, isolation_level='AUTOCOMMIT')
        with engine.connect() as conn:
            sql = text(f''' select * from public.delta_objects where name = '{name}' ''')
            output = conn.execute(sql).fetchall()[0]
        
        object_type = output[2]
        location = output[4]
            
        with engine.connect() as conn:
            sql = text(f''' 
                    delete from public.delta_objects_users
                    where object_id = (select id from public.delta_objects where name = '{name}')
            ''')
            conn.execute(sql)
                    
        with engine.connect() as conn:
            sql = text(f''' delete from  public.delta_objects where name = '{name}' ''')
            conn.execute(sql)
        
        if object_type == 'table':
            self.spark.sql(f'drop table {name}')
        elif object_type == 'view':
            self.spark.sql(f'drop view {name}')
        elif object_type == 'database':
            self.spark.sql(f'drop database {name}')
            name = name.lower()
            shutil.rmtree(f'/home/delta/.spark-warehouse/{name}.db')
        
        if len(location) > 0:
            shutil.rmtree(location)


    def check(self):
        return check(app = self)


    # create or alter objects 
    def __create_or_alter(self, script: str):
        try:
            postgres_conn = get_metastore_con()
            ids = []
            script = normalize_script(script)           
            engine = create_engine(postgres_conn, isolation_level='AUTOCOMMIT')
            info = extract_info_from_ddl_script(script)
            
            type = None
            name = None
            loc = None
            dt = datetime.datetime.now()
            type = info[0]
            name = info[1]
            loc = info[2]
    
            # store the object in the objects table in metastore
            with engine.connect() as conn:
                data = [{'script': str(script), 'type': str(type), 'name': name, 'loc': loc, 'username': self.username, 'dt': str(dt)}]
                sql = '''
                        insert into public.delta_objects (script, type, name, location, username, last_modified_date)
                        values (:script, :type, :name, :loc, :username, :dt) returning id
                    '''
                result = conn.execute(text(sql), data)
    
            # get id of the inserted object
            with engine.connect() as conn:
                sql = f'''
                        select id from delta_users where username = '{self.username}'
                    '''
                user_id = conn.execute(text(sql)).fetchone()[0]
                
            object_id = result.fetchone()[0]
            ids.append(object_id)
            access_level = 'rwc'
                
            # insert into delta_objects_users for the current user with access level
            with engine.connect() as conn:
                data = [{'user_id': user_id, 'object_id': object_id, 'access_level': access_level}]
                sql = '''
                        insert into public.delta_objects_users (user_id, object_id, access_level)
                        values (:user_id, :object_id, :access_level) returning id
                    '''
                result = conn.execute(text(sql), data)
                    
            ids.append(result.fetchone()[0])
            self.spark.sql(f'{script}')
        except:       
            with engine.connect() as conn:
                sql = f'''
                    delete from public.delta_objects where id = {ids[0]}
                '''
                conn.execute(text(sql))
            with engine.connect() as conn:
                sql = f'''
                    delete from public.delta_objects_users where id = {ids[1]}
                '''
                conn.execute(text(sql))


    def __check_access_level_of_a_user_for_a_script(self, script: str):
        postgres_conn = get_metastore_con()
        checks = []
        script = normalize_script(script)
        
        if 'create ' in script.lower():
            return True

        df = pd.read_sql_query(''' select name from delta_objects where "type" in ('table', 'view')  ''', postgres_conn)
        tables_and_views = self.spark.createDataFrame(df)    
       
        accessible_objects = [ [item[1], item[2]] for item in self.auth.get_access_level()]
        if len(accessible_objects) == 0:
            return False
            
        for item in tables_and_views.collect():
            # check if an object exists in the script
            if f' {item[0]} ' in script:
                ## if an object exists in the script, fetch its access level
                access_level = [row[1] for row in accessible_objects if row[0] == item[0]][0]
                
                if 'alter ' in script.lower() or 'drop ' in script.lower():
                    ## needs the change level
                    if 'c' in access_level:
                        checks.append([item[0], 'Change access' ,True])
                    else:
                        checks.append([item[0], 'Change access', False])
                
                elif 'insert ' in script.lower() or 'update ' in script.lower() or 'delete ' in script.lower():
                    ## needs the write level
                    if 'w' in access_level:
                        checks.append([item[0], 'Write access' ,True])
                    else:
                        checks.append([item[0], 'Write access' ,False])
                
                elif 'select ' in script.lower():
                    ## needs the read level
                    if 'r' in access_level:
                        checks.append([item[0], 'Read access' ,True])
                    else:
                        checks.append([item[0], 'Read access' ,False])
        if len(checks) == 0:
            return False
        for row in checks:
            if row[2] == False:
                return False
        return True


    def __sql(self, script: str):
        script = normalize_script(script)
    
        if 'create ' in script.lower():
            if self.__check_access_level_of_a_user_for_a_script(script):
                self.__create_or_alter(script)
            else:
                return '''You don't have enough permission.'''

        
        elif 'insert ' in script.lower() or 'update ' in script.lower() or 'delete ' in script.lower():
            if self.__check_access_level_of_a_user_for_a_script(script):
                self.spark.sql(script)
            else:
                return '''You don't have enough permission.'''

    
        elif 'select ' in script.lower():
            if self.__check_access_level_of_a_user_for_a_script(script):
                return self.spark.sql(script)
            else:
                return '''You don't have enough permission.'''
    
        else:
            print(script)
            print('Can not perform this script')





#########################
