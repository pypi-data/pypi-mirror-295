from .basics import *

class check:
    def __init__(self, app):
        self.app = app

    def check_column_is_not_null(self, query: str , column_name: str, save_check: bool = False):
        return check_column_is_not_null(self.app, query , column_name , save_check)

    def check_column_is_between(self, query: str , column_name: str, lower_bound: int ,upper_bound: int ,save_check: bool = False):
        return check_column_is_between(self.app, query, column_name, lower_bound, upper_bound, save_check)






