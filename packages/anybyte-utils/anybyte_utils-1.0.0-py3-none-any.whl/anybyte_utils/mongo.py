import pymongo


class MongoConn:
    def __init__(self, cluster_uri):
        self.cluster_uri = cluster_uri
        self.client = pymongo.MongoClient(self.cluster_uri)

    # Generic methods for MongoDB operations

    def get(self, db_name, collection_name, query=None):
        """Get a document from a MongoDB collection

        :param db_name: Database name
        :param collection_name: Collection name
        :param query: Query to filter documents
        :return: List of documents
        """
        db = self.client[db_name]
        collection = db[collection_name]
        return list(collection.find(query))

    def insert(self, db_name, collection_name, data):
        """Insert a document into a MongoDB collection

        :param db_name: Database name
        :param collection_name: Collection name
        :param data: Document to insert
        :return: True if document was inserted, else False
        """
        db = self.client[db_name]
        collection = db[collection_name]
        try:
            collection.insert_one(data)
        except Exception as e:
            print(f"Error inserting document: {e}")
            return False
        return True

    def update(self, db_name, collection_name, query, data):
        """
        Update a document in a MongoDB collection

        :param db_name: Database name
        :param collection_name: Collection name
        :param query: Query to filter documents
        :param data: Document to update
        """
        db = self.client[db_name]
        collection = db[collection_name]
        try:
            collection.update_one(query, {"$set": data})
        except Exception as e:
            print(f"Error updating document: {e}")
            return False
        return True

    def delete(self, db_name, collection_name, query):
        """
        Delete a document from a MongoDB collection

        :param db_name: Database name
        :param collection_name: Collection name
        :param query: Query to filter documents
        """
        db = self.client[db_name]
        collection = db[collection_name]
        try:
            collection.delete_one(query)
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False
        return True

    def list_databases(self):
        """
        List databases in the MongoDB cluster

        :return: List of database names
        """
        return self.client.list_database_names()

    def list_collections(self, db_name):
        """
        List collections in a MongoDB database

        :param db_name: Database name
        :return: List of collection names
        """
        db = self.client[db_name]
        return db.list_collection_names()

    def fetch_many(self, db_name, collection_name, query, limit=10):
        """
        Fetch multiple documents from a MongoDB collection

        :param db_name: Database name
        :param collection_name: Collection name
        :param query: Query to filter documents
        :param limit: Maximum number of documents to fetch
        :return: List of documents
        """
        db = self.client[db_name]
        collection = db[collection_name]
        return list(collection.find(query).limit(limit))

    def delete_many(self, db_name, collection_name, query):
        """
        Delete multiple documents from a MongoDB collection

        :param db_name: Database name
        :param collection_name: Collection name
        :param query: Query to filter documents
        """
        db = self.client[db_name]
        collection = db[collection_name]
        try:
            collection.delete_many(query)
        except Exception as e:
            print(f"Error deleting documents: {e}")
            return False
        return True

    def fetch_interactions(self, api_key, limit=None):
        """
        Fetch interactions from a MongoDB collection

        :param api_key: API key to search for interactions
        :param limit: Maximum number of interactions to fetch
        :return: List of interactions
        """
        db = self.client["interactions"]
        collection = db["interactions"]
        if limit:
            return list(collection.find({"api_key": api_key}).limit(limit))
        return list(collection.find({"api_key": api_key}))

    def fetch_interactions_paginated(self, api_key, page=1, limit=10):
        """
        Fetch interactions from a MongoDB collection in a paginated manner

        :param api_key: API key to search for interactions
        :param page: Page number
        :param limit: Maximum number of interactions per page
        :return: List of interactions
        """
        db = self.client["interactions"]
        collection = db["interactions"]
        skip = (page - 1) * limit
        return list(collection.find({"api_key": api_key}).skip(skip).limit(limit))

    def add_interaction(self, data):
        """
        Add an interaction to the MongoDB collection

        :param data: Interaction data
        :return: True if interaction was added, else False
        """
        db = self.client["interactions"]
        collection = db["interactions"]
        try:
            collection.insert_one(data)
        except Exception as e:
            print(f"Error adding interaction: {e}")
            return False
        return True
