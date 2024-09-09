from time import time
from ..helpers import *

def check_column_is_not_null(app, query: str , column_name: str, save_check: bool = False):
    t1 = time()
    # Use the native sql method so the authentication / authorization will work
    app.sql(query).createOrReplaceTempView('tmp')
        
    total = app.spark.sql('select * from tmp')
    failed = app.spark.sql(f'select * from tmp where {column_name} is null')
    total_count = total.count()
    failed_count = failed.count()
    t2 = time()
    summary = {
            'execution_time': t2 - t1,
            'user': app.username,
            'query': f'{query}',
            'check_type': 'is_not_null',
            'column_name': f'{column_name}',
            'total_count': total_count,
            'failed_count': failed_count,
            'success_percentage': ( (total_count-failed_count) / total_count) * 100
    }

    if save_check:
        save_checks(summary)
            
    return [summary, failed]


def check_column_is_between(app, query: str , column_name: str, lower_bound: int, upper_bound:int ,save_check: bool = False):
    t1 = time()
    # Use the native sql method so the authentication / authorization will work
    app.sql(query).createOrReplaceTempView('tmp')
        
    total = app.spark.sql('select * from tmp')
    failed = app.spark.sql(f'select * from tmp where {column_name} < {lower_bound} or {column_name} > {upper_bound}')
    total_count = total.count()
    failed_count = failed.count()
    t2 = time()
    summary = {
            'execution_time': t2 - t1,
            'user': app.username,
            'query': f'{query}',
            'check_type': 'check_column_is_between',
            'column_name': f'{column_name}',
            'total_count': total_count,
            'failed_count': failed_count,
            'success_percentage': ( (total_count-failed_count) / total_count) * 100
    }

    if save_check:
        save_checks(summary)
            
    return [summary, failed]