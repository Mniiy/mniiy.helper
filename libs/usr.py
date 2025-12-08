from database.UserDatabase import UserDatabase 

class exp:
    def __init__(self, Database:UserDatabase):
        self.database= Database
        self.exp= Database.fetchValue("exp")

class User():
    def __init__(self, discordID:int):
        from database.UserDatabase import UserDatabase 
        self.id= discordID
        self.database= UserDatabase(self)

    def addExp(self, qnt:int):
        self.Min(qnt)

        self.database.Addexp(qnt)



    @staticmethod
    def Min(self, number:int, ZeroAllowed:bool=False):
        min= (0 if not ZeroAllowed else 1)

        if number < min:
            raise ValueError(f"This vallue can't be less than {min}")