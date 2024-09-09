from pathlib import Path
from sqlalchemy import create_engine, text
import json
import datetime

from .config import *



# get the metastore connection string
def get_metastore_con():
    return f'postgresql://{pg_username}:{pg_password}@{pg_server}:{pg_port}/{pg_database}'

# normalize a given script
def normalize_script(script: str):
    script = script.replace('\n', ' ').strip().replace(';', '').replace('"', "'")
    new_words = [word.strip() for word in script.split(' ') if len(word.strip()) != 0]
    script = ' '.join(new_words)
    return f'{script} ;'

# get the absolute path
def get_absolute_path(system_path: str):
    return Path(system_path).resolve().__str__()

# extract the name, location and type of the object from the input script
def extract_info_from_ddl_script(script: str):
    script = normalize_script(script)
    if ' using delta location ' in script.lower():
        start = script.lower().find(' using delta location ') + 21
        end = len(script.lower())
        table_location = script[start:end].replace(';', '').strip().replace("'", "")
        table_location = get_absolute_path(table_location)
        if ' if not exists ' in script.lower():
            start = script.lower().find(' if not exists ') + 14
        else:
            start = script.lower().find(' table ') + 6
        end = script.find('(')
        table_name = script[start:end].strip()
        return ['table' ,table_name, table_location]
        
    elif ' view ' in script.lower():
        if ' if not exists ' in script.lower():
            start = script.lower().find(' if not exists ') + 14
        else:
            start = script.lower().find(' view ') + 5
        end = script.lower().find('as')    
        view_name = script[start:end].strip()
        return ['view', view_name, None]
    
    elif ' database ' in script.lower():
        db_name = script.replace(';', '').strip().split(' ')[-1]
        return ['database', db_name, None]

# create required objects
def initdb():
    try:
        postgres_conn = get_metastore_con()
        engine = create_engine(postgres_conn, isolation_level='AUTOCOMMIT')
        with engine.connect() as conn:
            sql = 'create table if not exists delta_objects ( id serial primary key, script text, type text, name text, location text, username text, last_modified_date timestamp )'
            conn.execute(text(sql))
        with engine.connect() as conn:
            sql = 'create unique index if not exists delta_objects_unique_name on delta_objects (name)'
            conn.execute(text(sql))
        with engine.connect() as conn:
            sql = 'create unique index if not exists delta_objects_unique_location on delta_objects (location) where location is not null'
            conn.execute(text(sql))
        with engine.connect() as conn:
            sql = 'create table if not exists delta_users ( id serial primary key, username varchar(500), password varchar(500) )'
            conn.execute(text(sql))
        with engine.connect() as conn:
            sql = 'create unique index if not exists delta_users_unique_username on delta_users (username)'
            conn.execute(text(sql))
        try:
            with engine.connect() as conn:
                sql = ''' insert into delta_users (username, "password") values ('admin', 'admin1234') '''
                conn.execute(text(sql))
            with engine.connect() as conn:
                sql = ''' insert into delta_users (username, "password") values ('test', 'test1234') '''
                conn.execute(text(sql))
        except:
            pass
        with engine.connect() as conn:
            sql = 'create table if not exists delta_objects_users ( id serial primary key, user_id int, object_id int, access_level varchar(3) ) '
            conn.execute(text(sql))
        with engine.connect() as conn:
            sql = 'create table if not exists delta_sources ( id serial4 NOT NULL, user_id int, source_object json, created_date timestamp)'
            conn.execute(text(sql))
        with engine.connect() as conn:
            sql = 'create table if not exists delta_checks (id serial4 not null, result json, runtime timestamp)'
            conn.execute(text(sql))
        with engine.connect() as conn:
            sql = '''
            create or replace view vw_checks as
            select 
                result->'execution_time' as execution_time,
                result -> 'user' as user,
                result -> 'query' as query,
                result -> 'check_type' as check_type,
                result -> 'column_name' as column_name,
                result -> 'total_count' as total_count,
                result -> 'failed_count' as failed_count,
                result -> 'success_percentage' as success_percentage
            from delta_checks
            '''
            conn.execute(text(sql))
        with engine.connect() as conn:
            sql = '''
            create or replace view vw_sources as
            select
                user_id,
                source_object -> 'user_username' as user_username,
                source_object -> 'user_password' as user_password,
                source_object -> 'spark_cpu_cores' as spark_cpu_cores,
                source_object -> 'spark_memory' as spark_memory,
                source_object -> 'source_name' as source_name,
                source_object -> 'server' as server,
                source_object -> 'database' as database,
                source_object -> 'db_username' as db_username,
                source_object -> 'db_password' as db_password,
                source_object -> 'port' as port,
                source_object -> 'source_type' as source_type,
                created_date 
            from delta_sources
            '''
            conn.execute(text(sql))
    except:
        return 'Metastore is not available. Please check your connection to the back-end database.'

# save the checks result
def save_checks(summary):
    postgres_conn = get_metastore_con()
    engine = create_engine(postgres_conn, isolation_level='AUTOCOMMIT')
    result = json.dumps(summary)
    
    sql = text('insert into delta_checks (result, runtime) values (:result, :runtime)')
    params = {"result": result, "runtime": datetime.datetime.now()}
    with engine.connect() as conn:
        conn.execute(sql, params)