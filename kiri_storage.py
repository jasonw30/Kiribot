import pathlib
from collections import namedtuple
import json
import unittest

#Do not touch anything on here :) - Kiri :3
DataTuple = namedtuple("DataTuple", ["file_location", "api_key", "secret_key", "user_data"])

class KiriSave:

    _base_save = {"main_data": {"file_location": None, "api_key": None, "secret_key": None, "user_data": {}}}
    _blank_data = {"xp": 0, "money": 0, "rank": None}

    def __init__(self, save_location: str, api_key: str, secret_key: str):
        self._api_key = api_key
        self._secret_key = secret_key
        self._data = self.setup(save_location)

        if self._data:
            self._file = self._data.file_location
            self._api_key = self._data.api_key
            self._secret_key = self._data.secret_key
            self._user_data = self._data.user_data

        print("[KiriSave] File Being Loaded")


    def setup(self, save_location) -> tuple:
        data_path = pathlib.Path(save_location)

        if data_path.exists() and data_path.is_dir():

            data_path = pathlib.Path(data_path) / "KiriStorage.json"

            if not data_path.exists():
                data_path.touch()
            

            with open(data_path, "r+") as kiri_file:
                
                if data_path.stat().st_size == 0:
                    self._base_save["main_data"]["file_location"] = str(pathlib.Path(save_location).absolute())
                    self._base_save["main_data"]["api_key"] = self._api_key
                    self._base_save["main_data"]["secret_key"] = self._secret_key
                    self._base_save["main_data"]["user_data"] = {}
                    kiri_file.write(json.dumps(self._base_save))
                
                kiri_file.seek(0)

                data = self.load_file(str(kiri_file.read()))

            return data

        else:

            print("[KiriSave] Error occured with the file location")
            return None
    
    def update_data(self, user):
        
        if self._user_data and (user in self._user_data):
            self._user_data[user]["xp"] = int(self._user_data[user]["xp"]) + 1
            #print(self._user_data)
            #print("Set")

            self.save_file()
        else:
            self._user_data[user] = self._blank_data
            self.update_data(user)
            #print("Updated")

    
    def get_data(self, user):
        
        if self._user_data and (user in self._user_data):
            return self._user_data[user]["xp"]
        else:
            return None


    def save_file(self):
        if self._file:
            current_path = pathlib.Path(self._file)
            print(current_path)
            if current_path.exists():

                file_path = current_path / "KiriStorage.json"
                
                if file_path.exists():
                    #print("[KiriSave] Checker File Passed.")

                    with open(file_path, "w+") as kiri_file:
                        self._base_save["main_data"]["file_location"] = self._file
                        self._base_save["main_data"]["api_key"] = self._api_key
                        self._base_save["main_data"]["secret_key"] = self._secret_key
                        self._base_save["main_data"]["user_data"] = self._user_data
                        kiri_file.write(json.dumps(self._base_save))
                    
                else:
                    pass
                    #print("[KiriSave] File has been saved successfully.")


    @staticmethod
    def load_file(file_data: str):
        try:
            data = json.loads(file_data)
            main_data = data["main_data"]
            file_location = main_data["file_location"]
            api_key = main_data["api_key"]
            secret_key = main_data["secret_key"]
            user_data = main_data["user_data"]

            print("[KiriSave] Loaded File")
            return DataTuple(file_location, api_key, secret_key, user_data)
        except (json.JSONDecodeError) as decode_error:
            print("[KiriSave] " + str(decode_error))


if __name__ == "__main__":
    print("[KiriStorage] Module Loaded For Testing")

    class KiriTest(unittest.TestCase):
        
        def test_practice(self):
            kiri_test = KiriSave(".", "test", "test")

    unittest.main()