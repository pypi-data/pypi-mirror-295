from .helpers import *
from sqlalchemy import create_engine, text

class auth:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def login(self):
        postgres_conn = get_metastore_con()
        engine = create_engine(postgres_conn, isolation_level='AUTOCOMMIT')
        sql = f'''select * from delta_users where username = '{self.username}' and password = '{self.password}' '''
        with engine.connect() as conn:
            row = conn.execute(text(sql)).fetchone()
        if not row:
            return False
        else:
            return True


    def get_access_level(self):
        postgres_conn = get_metastore_con()
        '''
            read: r
            create, insert, update, delete: w
            alter, drop : c (changes just for admins)
        '''
        sql = f'''
                select
                     dlo.script as script, 
                     dlo."name" as name,
                     case when dlo."type" = 'database' then 'rwc' else dlou.access_level end as access_level
                from delta_objects_users dlou
                inner join delta_objects dlo on dlou.object_id = dlo.id
                inner join delta_users du on du.id = dlou.user_id
                where du.username = '{self.username}'
                order by dlo.last_modified_date asc
            '''
        engine = create_engine(postgres_conn, isolation_level='AUTOCOMMIT')
        with engine.connect() as conn:
            return conn.execute(text(sql))