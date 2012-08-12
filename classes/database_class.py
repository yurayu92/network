import MySQLdb

class database:
    
    cursor = None
    
    def __init__(self):
        db = MySQLdb.connect(host='localhost',
                            user='root',
                            passwd='itdxer',
                            db='network', 
                            cursorclass=MySQLdb.cursors.DictCursor)
        self.cursor = db.cursor()
        self.cursor.execute("SET NAMES utf8")
        
    def fetchAll(self, query):
        select = self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetchOne(self, query):
        select = self.cursor.execute(query)
        return self.cursor.fetchone()
    
    def fetchMany(self, query, limit = 10):
        select = self.cursor.execute(query)
        return self.cursor.fetchmany(limit)
    
    def count(self, query):
        count = self.cursor.execute(query)
        return self.cursor.rowcount