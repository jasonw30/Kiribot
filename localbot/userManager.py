import math
from . import MongoDB

Database = MongoDB()
CACHE_DATA = {}

class UserData:
    
    def __init__(self, user_id=None, exp=0, money=0):
        self.user_id = user_id
        self.exp = exp
        self.money = money
    
class UserDataManager:

    @staticmethod
    def get_user_stats(user_id) -> None:
        """
        Retrieves and converts user data if exists to a UserData object, else make an empty one.
        """
        if str(user_id) in CACHE_DATA.keys():
            print("got cached")
            return CACHE_DATA[str(user_id)]

        query_found = Database.get_query(str(user_id))
        if not query_found:
            CACHE_DATA[str(user_id)] = UserData(user_id)
        else:
            CACHE_DATA[str(user_id)] = UserData(user_id, exp=query_found['exp'], money=query_found['money'])
    
        return CACHE_DATA[str(user_id)]


    @staticmethod
    def save_user_stats(user_input: UserData):
        query_found = Database.get_query(user_input.user_id)
        if query_found:
            Database.delete_query(user_input.user_id)
            Database.save_data(user_input.__dict__)
        else:
            Database.save_data(user_input.__dict__)

    @staticmethod
    def clear_user_stats(user_id):
        query_found = Database.get_query(user_id)
        if query_found:
            Database.delete_query(str(user_id))
            print("Found user. Cleared User Data.")
        else:
            print("Cannot delete user, not found.")

    @staticmethod
    def user_level(user_data: UserData):
        return math.floor(user_data.exp / 100)
    
    @staticmethod
    def update_money(user_data: UserData, updateCurrency: int):
        user_data.money = updateCurrency

    @staticmethod
    def update_exp(user_data: UserData, updateXP: int):
        user_data.exp = updateXP
    
    @staticmethod
    def async_save():
        print("Starting Async Save Process")
        print(CACHE_DATA)
        for userData in CACHE_DATA.items():
            print("Saving:", userData[0])
            UserDataManager.save_user_stats(userData[1])
        print("Finished Saving Data...")
