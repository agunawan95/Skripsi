import pymysql


class Database:
    con = None
    cur = None

    def __init__(self):
        self.con = pymysql.connect(host='localhost', user='root', password='', db='auto_analytics')
        self.cur = self.con.cursor(pymysql.cursors.DictCursor)
