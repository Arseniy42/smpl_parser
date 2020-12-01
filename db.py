import os
import sqlite3

from sqlite3 import Error
from datetime import datetime


class Database:

    conn = None
    curs = None

    def __init__(self):
        self.conn = self.create_db()
        self.curs = self.conn.cursor()
        self.create_table_recipe()

    def create_db(self):
        if not os.path.exists('db'):
            os.mkdir('db')

        try:
            conn = sqlite3.connect('db/{db_name}.db'.format(db_name=datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        except Error as e:
            print(e)

        return conn

    def create_table_recipe(self):
        try:
            self.curs.execute("""
                CREATE TABLE recipe (
                    id integer primary key autoincrement,
                    recipe_name varchar(255),
                    recipe_url varchar(255),
                    person_name varchar(255),
                    person_id int,
                    recipe_description longtext,
                    kkal_value int,
                    kkal_unit varchar(255),
                    kkal_percent varchar(255)
                );
            """)
        except Error as e:
            print(e)

    def insert(self, record_list):
        insert_query = 'INSERT INTO recipe (' \
                           'recipe_name, recipe_url, person_name, person_id, recipe_description,' \
                           'kkal_value, kkal_unit, kkal_percent' \
                       ')' \
                       'values (?, ?, ?, ?, ?, ?, ?, ?);'
        self.curs.execute(insert_query, record_list)
        self.conn.commit()
