import pymysql
from .sqlsetting import *
def select(sql):
    db=pymysql.connect(SQL_HOST, SQL_USER, SQL_PASS, SQL_NAME,charset="utf8",cursorclass=(pymysql.cursors.DictCursor))
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    return result
def one(sql):
    db = pymysql.connect(SQL_HOST, SQL_USER, SQL_PASS, SQL_NAME, charset="utf8",
                         cursorclass=(pymysql.cursors.DictCursor))
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    db.close()
    return result
def exec(sql):
    db = pymysql.connect(SQL_HOST, SQL_USER, SQL_PASS, SQL_NAME, charset="utf8",
                         cursorclass=(pymysql.cursors.DictCursor))
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()
class sql:
    def __init__(self):
        self.db=pymysql.connect(SQL_HOST, SQL_USER, SQL_PASS, SQL_NAME, charset="utf8",
                         cursorclass=(pymysql.cursors.DictCursor))
        self.cursor=self.db.cursor()
    def select(self,sql,args=[]):
        self.cursor.execute(sql,args)
        result = self.cursor.fetchall()
        return result
    def one(self,sql,args=[]):
        self.cursor.execute(sql,args)
        result = self.cursor.fetchone()
        return result
    def exec(self,sql,args=[]):
        self.cursor.execute(sql,args)
        self.db.commit()
    def Inset_id(self,sql,args):
        self.cursor.execute(sql,args)
        id=self.db.insert_id()
        self.db.commit()
        return id
    def exec_many(self,sql,args):
        self.cursor.executemany(sql, args)
        self.db.commit()
    def delete(self,sql,args=[]):
        self.cursor.execute(sql,args)
        self.db.commit()
    def update(self,sql,args=[]):
        self.cursor.execute(sql,args)
        self.db.commit()
    def close(self):
        self.cursor.close()
        self.db.close()
