import pymongo
from config import MONGO_FULL_URI


class MongoDB(object):
    """
    Class for uploading data to MongoDB.
    """
    def __init__(self, database, collection):
        """
        Initialize the class.
        """
        self.client = pymongo.MongoClient(MONGO_FULL_URI)
        self.database = self.client[database]
        self.collection = self.database[collection]
    
    def Change_Database(self, database):
        """
        Change the database.
        """
        self.database = self.client[database]
        return True
    
    def Change_Collection(self, collection):
        """
        Change the collection.
        """
        self.collection = self.database[collection]
        return True
    

    def Upload(self, json_data):
        """
        Upload the data to MongoDB.
        """
        try:
            self.collection.insert_many(json_data)
            return True
        except pymongo.errors.BulkWriteError as e:
            print(f"Error uploading data: {e.details}")
            return False
    
    def Disconnect(self):
        """
        Disconnect from MongoDB.
        """
        self.client.close()
        return True
    

    def Query(self, query):
        """
        Query the MongoDB database.
        """
        return list(self.collection.find(query))
    

    def Query_One(self, query):
        """
        Query the MongoDB database for a single document.
        """
        return self.collection.find_one(query)


    def Delete_Many(self, query):
        """
        Delete data from MongoDB.
        """
        self.collection.delete_many(query)
        return True
    

    def Delete_One(self, query):
        """
        Delete data from MongoDB.
        """
        self.collection.delete_one(query)
        return True
    

    def Update_Many(self, query, update):
        """
        Update data in MongoDB.
        """
        results = self.collection.update_many(query, update)
        return results.to_dict()
    

    def Update_One(self, query, update):
        """
        Update data in MongoDB.
        """
        result = self.collection.update_one(query, update)
        return result.to_dict()


    def Update_Or_Upsert(self, query, update_dict):
        """
        Updates a MongoDB document in a collection based on a query parameter, using update_one method.
        If no document matches the query, a new document is inserted using insert_one method.
        :param query: A dictionary specifying the query used to find the document to update
        :param update_dict: A dictionary specifying the new values to set in the document
        """
        result = self.collection.update_one(query, {'$set': update_dict}, upsert=True)


    def Insert_One(self, data):
        """
        Insert a single document into MongoDB.
        """
        result = self.collection.insert_one(data)
        return result.to_dict()
    
    def Insert_Many(self, data):
        """
        Insert many documents into MongoDB.
        """
        results = self.collection.insert_many(data)
        return results.to_dict()


    def Count(self, query):
        """
        Count the number of documents in MongoDB.
        """
        return self.collection.count_documents(query)
    
    
    def Distinct(self, field, query):
        """
        Get the distinct values for a field in MongoDB.
        """
        return self.collection.distinct(field, query)
    

    def Aggregate(self, pipeline):
        """
        Aggregate data in MongoDB.
        """
        return self.collection.aggregate(pipeline)
    