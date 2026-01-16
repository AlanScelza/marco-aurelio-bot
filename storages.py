#!/usr/bin/env/ python3

import os
import logging
from pymongo import MongoClient

logger = logging.getLogger(__name__)

class MongoStorage(object):
    """ Clase de la interfaz para la conexion a la base de datos de Mongo. """

    def __init__(self):
        logger.info('Inicializando MongoStorage')

        if os.environ.get("MONGO_STORAGE_URL"):
            self.client = MongoClient(os.environ.get("MONGO_STORAGE_URL"))
        else:
            logger.error('No se definió MONGO_STORAGE_URL.')
            raise ValueError("Debe definirse MONGO_STORAGE_URL")

        self.db = self.client[os.environ.get("MONGO_STORAGE_DB")]
        self.db.collection = self.db[os.environ.get("MONGO_STORAGE_COLLECTION")]

    def get(self, key=None):
        if key:
            value = self.db.collection.find_one({'_id': key})
        else:
             value = list(self.db.collection.find())
        return value
    
    def insert(self, data):
        assert isinstance(data, dict)
        data = dict(data)
        self.db.collection.insert_one(data)

    def update(self, key, data):
        assert isinstance(data, dict)
        data = dict(data)
        self.db.collection.update_one({'_id': key}, {'$set': data}, upsert=True)

    def delete(self, query, query_delete):
        result = self.db.collection.update_one(query, query_delete)
        return result

if __name__ == '__main__':
    import sys
    import json
    storage = MongoStorage()

    value = storage.get(sys.argv[1])
    print(json.dumps(value, indent=True))

