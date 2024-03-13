import pymongo
import configparser
from pathlib import Path
from pymongo.write_concern import WriteConcern

config = configparser.ConfigParser()
config.read(Path(".").parent / Path("configuration.ini"))
DATASAVE = config.get('MongoDB', 'Link')
DATABASE = config.get('MongoDB', 'Database')
COLLECTION = config.get('MongoDB', 'Collection')

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
        clientCollection = clientCollection.with_options(write_concern=WriteConcern(w='majority'))

        return client, clientCollection
    
    def save_data(self, query_save: dict):
        """
        Use .json format to save data
        """
        client, clientCollection = self.__get_collection()
        result = clientCollection.insert_one(query_save)
        client.close()
    
    def retreive_all_data(self):
        """
        Returns All of the Data in the Database
        """
        client, clientCollection = self.__get_collection()
        all_data = clientCollection.find()
        dict_data = [data for data in all_data]
        client.close()
        return dict_data

    def update_query(self, query_input: dict, new_query_input: dict):
        """
        Updates a single element
        """
        client, clientCollection = self.__get_collection()
        clientCollection.update_one(query_input, new_query_input)
        client.close()

    def delete_query(self, string_input):
        """
        Delete a Single Element
        """
        BASE_QUERY = {"user_id": string_input} 
        client, clientCollection = self.__get_collection()
        clientCollection.delete_one(BASE_QUERY)
        client.close()

    def remove_collection(self):
        """
        Removes all of the data in the collection!
        """
        client, clientCollection = self.__get_collection()
        clientCollection.delete_many({})
        client.close()
    
    def get_query(self, string_input):
        """
        Gets all of the documents given a string input
        """
        BASE_QUERY = {"user_id": string_input} 
        client, clientCollection = self.__get_collection()
        query_result = clientCollection.find_one(BASE_QUERY)
        client.close()
        return query_result

    def insert_all(self, list_input:list[dict]):
        """
        Given a list of documents or dictionaries in this case, it will upload all of the
        Dictionaries into MongoDB at once rather than one at a time.
        """
        client, clientCollection = self.__get_collection()
        query_result = clientCollection.insert_many(list_input)
        client.close()
        return query_result