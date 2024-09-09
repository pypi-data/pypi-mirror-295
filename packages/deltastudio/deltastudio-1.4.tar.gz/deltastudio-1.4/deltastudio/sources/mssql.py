import math
from tqdm import tqdm
from time import time
import json
from sqlalchemy import create_engine, text
import datetime
from ..helpers import *

class mssql:
    def __init__(self, app ,source_name: str, server: str, database: str, db_username: str, db_password: str, port: str = '1433'):
        self.source_name = source_name
        self.server = server
        self.database = database
        self.username = db_username
        self.password = db_password
        if not port:
            self.port = '1433'
        else:
            self.port = port
        self.sqlsUrl = f'jdbc:sqlserver://{self.server}:{self.port};database={self.database};trustServerCertificate=true'
        self.jdbc_options = {
            "url": self.sqlsUrl,
            "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
            "user": self.username,
            "password": self.password
        }
        self.app = app

    
    def read_mssql_query_to_spark_dataframe(self, query: str):
        qryStr = f'({query}) t'
        return self.app.spark.read.format('jdbc').option('dbtable', qryStr ).options(**self.jdbc_options).load()
        

    def create_deltatable_from_spark_dataframe(self, df, location: str, table_full_name: str):
        if len(location) == 0:
            print('Location can not be empty.')
            return
        if len(table_full_name) == 0:
            print('Table name (including database name) can not be empty.')
            return

        script = f'create table if not exists {table_full_name} ( '
        for row in df.dtypes:
            script += f'{row[0]} {row[1]},'
        script = script[0: len(script)-1]
        script += f''') using delta location '{location}' '''
        self.app.sql(script)
        

    def write_spark_dataframe_to_deltatable(self, df, target_table: str, chunk_size: int = 0):
        df.createOrReplaceTempView('tmp_tbl')
        if chunk_size == 0:
            self.app.sql(f'''
                insert into {target_table}
                select * from tmp_tbl
            ''')
        else:
            iter = 0
            cnt = df.count()
            total = math.ceil(cnt / chunk_size)
    
            with tqdm(total = total) as pbar:
                while iter < total:
                    self.app.sql(f'''
                                insert into {target_table}
                                select * from tmp_tbl limit {chunk_size} offset {iter*chunk_size}
                            ''')
                    iter += 1
                    pbar.update(1)


    def el_mssql_query(self, query: str, location: str = '', table_full_name: str = '', mode = 'append' , chunk_size: int = 0):
        t1 = time()
        print('Reading the data ...')
        try:
            df = self.read_mssql_query_to_spark_dataframe(query)
        except:
            return 'Source is not available.'
            
        print('Creating the delta table ...')
        try:
            self.create_deltatable_from_spark_dataframe(df, location, table_full_name)
        except:
            return 'Table with this name or location exists.'
            
        print('Writing the data into the delta table ...')
        
        if mode.lower().strip() == 'append':
            try:
                self.write_spark_dataframe_to_deltatable(df, table_full_name, chunk_size)
            except:
                return 'Writing the data into the table encounters error.'
            t2 = time()
            print(f'Finished. Execution time: {t2 - t1}')
        elif mode.lower().strip() == 'overwrite':
            try:
                try:
                    self.app.sql(f''' delete from {table_full_name} ''')
                except:
                    pass
                self.write_spark_dataframe_to_deltatable(df, table_full_name, chunk_size)
            except:
                return 'Writing the data into the table encounters error.'
            t2 = time()
            print(f'Finished. Execution time: {t2 - t1}')
        else:
            return 'Unknown mode. Please try one of the overwrite or append. The default value is append. '

    def __str__(self):
        return {
            'user_username': f'{self.app.username}',
            'user_password': f'{self.app.password}',
            'spark_cpu_cores': f'{self.app.spark_cpu_cores}',
            'spark_memory': f'{self.app.spark_memory}',
            'source_name': f'{self.source_name}',
            'server': f'{self.server}',
            'database': f'{self.database}',
            'db_username': f'{self.username}',
            'db_password': f'{self.password}',
            'port': f'{self.port}',
            'source_type': 'mssql'
        }
        
    def save(self):
        postgres_conn = get_metastore_con()
        engine = create_engine(postgres_conn, isolation_level='AUTOCOMMIT')
        source_object = json.dumps(self.__str__())
        with engine.connect() as conn:
            user_id = conn.execute(text(f'''select id from delta_users where username  = '{self.app.username}' ''')).fetchone()[0]

        sql = text('insert into delta_sources (user_id, source_object, created_date) values (:user_id, :source_object, :created_date)')
        params = {"user_id": user_id, "source_object": source_object, "created_date": datetime.datetime.now()}
        with engine.connect() as conn:
            conn.execute(sql, params)