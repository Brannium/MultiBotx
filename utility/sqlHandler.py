import json
import os

import psycopg2
from nested_dict import nested_dict
from psycopg2 import sql

DEFAULT_TABLE = 'multibot'
CONFIG = 'config'
STATS = 'stats'

class MyDatabase():
    def __init__(self):
        self.user = os.environ.get('db_user')
        self.password = os.environ.get('db_password')
        self.host = os.environ.get('db_host')
        self.port = os.environ.get('db_port')
        self.database = os.environ.get('db_database')
        self.con = None;
        self.cursor = None;

    '''
    Connect to database using credentials specified in systemvariables
    '''
    def connect(self):
        try:
            self.con = psycopg2.connect(user=self.user,
                                        password=self.password,
                                        host=self.host,
                                        port=self.port,
                                        database=self.database)
            self.con.set_session(autocommit=True)
            self.cursor = self.con.cursor()
        except (Exception, psycopg2.Error) as error:
            print('Error while connecting to PostgreSQL)', error)

    '''
    Close connection to database
    '''
    def close(self):
        if(self.con):
            self.cursor.close()
            self.con.close()

    '''
    Print content of given table, table is the name of the table
    '''
    def print_table(self, table):
        self.connect()
        print('Content of table \'%s\':')
        self.cursor.execute('SELECT * FROM ' + table)
        for record in self.cursor:
            print(record)
        self.close()

    '''
    Returns 1 when serverid is existing in table and 0 when not
    '''
    def serverid_exists(self, table, serverid):
        self.connect()
        self.cursor.execute(sql.SQL('SELECT COUNT(1) FROM {} WHERE serverid=%s').format(
            sql.Identifier(table)),
            [serverid])
        return self.cursor.fetchone()[0]

    '''
    Returns a nested_dict with the data requested
    '''
    def get(self, table, column, serverid):
        if self.serverid_exists(table, serverid):
            self.connect()
            self.cursor.execute(sql.SQL('SELECT {} FROM {} WHERE serverid=%s').format(
                sql.Identifier(column),
                sql.Identifier(table)),
                [serverid])
            raw = self.cursor.fetchone()
            self.close()
            if raw[0] is not None:
                try:
                    return nested_dict(raw[0])
                except Exception as e:
                    print('Exception while getting config: %s' % e)
        return nested_dict()

    '''
    Saves a nested_dict as json data at given place
    '''
    def set(self, table, column, serverid, data):
        self.connect()
        if self.serverid_exists(table, serverid):
            self.cursor.execute(sql.SQL('UPDATE {} SET {}=%s WHERE serverid=%s').format(
                sql.Identifier(table),
                sql.Identifier(column)),
                [json.dumps(data, sort_keys=True), serverid])
        else:
            self.cursor.execute(sql.SQL('INSERT INTO {}(serverid, {}) VALUES(%s, %s)').format(
                sql.Identifier(table),
                sql.Identifier(column)),
                [serverid, json.dumps(data, sort_keys=True)])

    # ####
    # Some methods with default values for easier access from other classes
    # ####
    def get_config(self, serverid):
        return self.get(DEFAULT_TABLE, CONFIG, serverid)

    def get_stats(self, serverid):
        return self.get(DEFAULT_TABLE, STATS, serverid)

    def save_config(self, serverid, data):
        self.set(DEFAULT_TABLE, CONFIG, serverid, data)

    def save_stats(self, serverid, data):
        self.set(DEFAULT_TABLE, STATS, serverid, data)
