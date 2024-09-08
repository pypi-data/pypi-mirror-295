import mysql.connector as mysql_connector
import sqlite3 as sqlite

modes = ['mysql', 'sqlite']

class SQL_Class:

    def __init__(self, mode='mysql', db=None, cursor=None, tables=None):
        self.cursor = cursor
        self.db = db
        self.mode = mode
        self.tables = tables

    def __del__(self):
        try:
            self.cursor.close()
            self.db.close()
        except Exception:
            pass

    def ifconnected(self):
        if self.cursor == None:
            return False
        else:
            return True

    def table_str(self, tabels=None, return_first=False):
        if tabels is None:
            tabels = [x for x in self.tables]
        for x in range(len(tabels)):
            if self.mode == 'mysql':
                tabels[x] = f'{tabels[x]}'
            if self.mode == 'sqlite':
                tabels[x] = f'{tabels[x]}'
        if not return_first:
            return ', '.join(tabels)
        else:
            return tabels[0]

    def select_str(self, *args):
        if len(args) == 0:
            select = '*'
        else:
            select = ', '.join(args)
        return select

    def where_construct(self, **kwargs):
        elements = list()
        for x in kwargs:
            elements.append(f"{x} = '{kwargs[x]}'")
        elements = ' and '.join(elements)
        return elements

    def reset_auto_increment(self):
        self.Execute_SQL_Command(f'ALTER TABLE `{self.table_str()}`  AUTO_INCREMENT = 1')
        self.db.commit()

    def clear_table(self):
        self.Execute_SQL_Command(f'DELETE FROM `{self.table_str()}`')
        self.db.commit()

    def basic_read(self, tabels=None, *args, **kwargs):
        if not self.ifconnected():
            raise NotConnected
        tabels_str = self.table_str(tabels)
        select = self.select_str(*args)
        elements = self.where_construct(**kwargs)
        if kwargs == {}:
            Abfrage = f'SELECT {select} FROM {tabels_str}'
        else:
            Abfrage = f'SELECT {select} FROM {tabels_str} WHERE {elements}'
        Return = self.Execute_SQL_Command(Abfrage)
        return Return

    def basic_write(self, tabels=None, **kwargs):
        if not self.ifconnected():
            raise NotConnected
        tabels_str = self.table_str(tabels, True)
        colums = []
        for x in kwargs:
            colums.append(x)
        values = []
        for x in kwargs:
            values.append(kwargs[x])
        for x in range(len(values)):
            values[x] = f"'{values[x]}'"
        colums = ', '.join(colums)
        values = ', '.join(values)
        Abfrage = f'INSERT INTO {tabels_str} ({colums}) VALUES ({values})'
        self.Execute_SQL_Command(Abfrage)
        self.db.commit()

    def basic_delete(self, tabels=None, **kwargs):
        if not self.ifconnected():
            raise NotConnected
        tabels_str = self.table_str(tabels, True)
        elements = self.where_construct(**kwargs)
        Abfrage = f'DELETE FROM {tabels_str} WHERE {elements}'
        self.Execute_SQL_Command(Abfrage)
        self.db.commit()

    def Execute_SQL_Command(self, command: str):
        print(command)
        self.cursor.execute(command)
        return self.cursor.fetchall()

class sqlite3(SQL_Class):

    def __init__(self, path:str, tables:list):
        self.tables = tables
        self.db = self.connect_sqlite(path)
        self.cursor = self.db.cursor()
        super().__init__('sqlite', self.db, self.cursor, self.tables)

    def connect_sqlite(self, path):
        return sqlite.connect(path)

class mysql(SQL_Class):

    def __init__(self, host:str, user:str, password:str, database:str, tables:list):
        self.db = self.connect_mysql(host, user, password, database)
        self.cursor = self.db.cursor()
        super().__init__(db=self.db, cursor=self.cursor, tables=tables)

    def connect_mysql(self, host, user, password, database):
        return mysql_connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
        )

class NotConnected(Exception):

    pass

class NotSupportedMode(Exception):

    pass