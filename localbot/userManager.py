from mongoEngine import MongoDB

class UserData:
    
    def __init__(self):
        self.user_id = None
        self.level = 0
        self.xp = 0
        self.message_history = []

    def get_user_data(self):
        database = MongoDB()
        saved_data = database.get_query(self.user_id)
        saved_data["user_id"] = 