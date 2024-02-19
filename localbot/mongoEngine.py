import pymongo
import configparser
from pathlib import Path

config = configparser.ConfigParser()
config.read(Path(".").parent / Path("configuration.ini"))
DATASAVE = config.get('MongoDB', 'Link')
DATABASE = config.get('MongoDB', 'Database')
COLLECTION = config.get('MongoDB', 'UserData')

class MongoDB:

    def __init__(self, client=DATASAVE, database=DATABASE, collection=COLLECTION):
        """
        Initalizes the mongodb
        """
        self.client = client
        self.database = database
        self.collection = collection
        print(f"[MongoDB Manager] Datasave -> {DATASAVE}")
        print(f"[MongoDB Manager] Database -> {DATABASE}")
        print(f"[MongoDB Manager] Database Collection -> {COLLECTION}")
        print(f"[MongoDB Manager] Successfully Setup")

    def __get_collection(self):
        """
        Gets the collection of the MongoDB database
        """
        client = pymongo.MongoClient(self.client)
        clientDatabase = client[self.database]
        clientCollection = clientDatabase[self.collection]
        return client, clientCollection
        
    
    def save_data(self, query_save: dict):
        """
        Use .json format to save data
        """
        client, clientCollection = self.__get_collection()
        clientCollection.insert_one(query_save)
        print(f"[MongoDB Manager] Saved Data!")
        client.close()
    
    def retreive_all_data(self):
        """
        Returns All of the Data in the Database
        """
        client, clientCollection = self.__get_collection()
        all_data = clientCollection.find()
        dict_data = [data for data in all_data]
        client.close()
        print(f"[MongoDB Manager] Obtained All Data")
        return dict_data

    def update_query(self, query_input: dict, new_query_input: dict):
        """
        Updates a single element
        """
        client, clientCollection = self.__get_collection()
        update_result = clientCollection.update_one(query_input, new_query_input)
        client.close()
        print(update_result)

    def delete_query(self, query_input: dict):
        """
        Delete a Single Element
        """
        client, clientCollection = self.__get_collection()
        update_result = clientCollection.delete_one(query_input)
        client.close()
        print(update_result)

    def remove_collection(self):
        """
        Removes all of the data in the collection!
        """
        client, clientCollection = self.__get_collection()
        query_result = clientCollection.delete_many({})
        client.close()
        print(f"[MongoDB Manager] Deleted a total of {query_result.deleted_count} documents.")
    
    def get_query(self, string_input):
        """
        Gets all of the documents given a string input
        """
        BASE_QUERY = {string_input: {"$exists": True}} 
        client, clientCollection = self.__get_collection()
        query_result = clientCollection.find_one(BASE_QUERY)
        client.close()
        print(f"[MongoDB Manager] Found Document!")
        return query_result

    def insert_all(self, list_input:list[dict]):
        """
        Given a list of documents or dictionaries in this case, it will upload all of the
        Dictionaries into MongoDB at once rather than one at a time.
        """
        client, clientCollection = self.__get_collection()
        query_result = clientCollection.insert_many(list_input)
        print(f"[MongoDB Manager] Successfully uploaded all of the documents!")
        client.close()
        return query_result


if __name__ == "__main__":
    #examples of what you can do. Might have to whitelist IP Address for it to work, essentially you can store your string client, put database name and collection and it
    #should work
    CurData = MongoDB()
    CurData.save_data({'docID': 1, 'terms': ["hello", "world"]})
    res = CurData.retreive_all_data()
    print(res)
    CurData.remove_collection()
    #-------------------TESTING------------------#
    print("-----------------------TESTING-------------------------")
    CurData.save_data({"Hello": [(1, 6, [1, 9, 27], 8.99, 10)]})
    CurData.save_data({"Word": [(1, 6, [1, 9, 27], 8.99, 10)]})
    CurData.save_data({"exampleToken": [(1, 6, [1, 9, 27], 8.99, 10)]})
    CurData.save_data({"tokenStorage": [(1, 6, [1, 9, 27], 8.99, 10)]})
    resultFound = CurData.get_documents("Hello")
    print(resultFound)
    res = CurData.retreive_all_data()
    CurData.remove_collection()

