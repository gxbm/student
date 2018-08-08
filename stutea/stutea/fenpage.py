import math
import pymysql
from .sqlsetting import *
class page:
    #一个是start，一个是end
    def __init__(self,sql,num=5):
        self.db = pymysql.connect(SQL_HOST, SQL_USER, SQL_PASS, SQL_NAME, charset="utf8",
                                  cursorclass=(pymysql.cursors.DictCursor))
        self.cursor = self.db.cursor()
        self.currentindex=1
        self.page=10
        self.num=num
        self.sql=sql
        self.cursor.execute(self.sql)
        self.total=self.cursor.fetchall()
    def startindex(self):
        self.startindex=(self.currentindex-1)*self.num
        return self.startindex
    def pagenum(self):
        self.page=math.ceil(self.total/self.num)

