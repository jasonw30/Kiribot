from mongoEngine import MongoDB

class UserData:
    
    def __init__(self):
        self.user_id = None
        self.level = 0
        self.xp = 0
        self.message_history = []

    def get_user_stats(self):
        pass

    def save_user_stats(self):
        pass

    def clear_user_stats(self):
        pass