import sqlite3
conn= sqlite3.connect("database.db")
conn.row_factory = sqlite3.Row


class UserDatabase():
    def __init__(self, id):
        self.id= id
        self.cur= conn.cursor()

    def fetchValue(self):
        pass

    
    def register(self):
        pass

    def Addexp(self, new:int):
        query= "UPDATE "


    def LevelUp(self):
        pass