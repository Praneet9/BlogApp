from pymongo import MongoClient
from bson.objectid import ObjectId


def register_user(User):
    data = {'username': User.username,
            'email': User.email,
            'password': User.password,
            'posts': User.posts,
            'image_file': User.image_file}
    user_collection.insert_one(data)

def check_user(email):
    result = user_collection.find_one({'email': email})
    return result

def validate(key, value):
    results = user_collection.find_one({key: value})
    return results

def get_user(user_id):
    results = user_collection.find_one({'_id': ObjectId(user_id)})
    return results

def updateAccount(old, new):
    new = {'$set': new}
    user_collection.update_one(old, new)

def _getConnection():
    client = MongoClient('localhost:27017')
    return client

def _getDB(client):
    db = client.FlaskBlog
    return db

def _getCollection(collection_name, db):
    collection = db[collection_name]
    return collection

def closeConnection(client):
    client.close()

global user_collection, post_collection

client = _getConnection()
db = _getDB(client)
user_collection = _getCollection('users', db)
post_collection = _getCollection('posts', db)

##Database Helper functions
# def insert_data(collection, args_dict):
#     client = getConnection()
#     db = getDB(client)
#     collection_name = getCollection(collection, db)
#     '''
#     db_name -> string i.e name of the db
#     args_dict -> a dictionary of entries in db
#     '''
#     collection_name.insert_one(args_dict)
    
#     closeConnection(client)

# def read_data(collection):
#     client = getConnection()
#     db = getDB(client)
#     collection_name = getCollection(collection, db)
#     '''
#     returns a cursor of objects
#     which can be iterated and printed
#     '''
#     cols = collection_name.find({})
#     closeConnection(client)
#     return cols

# #Update in data base
# def update_data(collection, idno, updation):
#     client = getConnection()
#     db = getDB(client)
#     collection_name = getCollection(collection, db)
#     '''
#     db_name -> string
#     idno -> id number of database entry in dict
#     '''
#     collection_name.update_one(idno, updation)
#     closeConnection(client)

# def delete_row(collection, idno):
#     client = getConnection()
#     db = getDB(client)
#     collection_name = getCollection(collection, db)
#     '''
#     Deletes the complete row
#     idno must be a dict {idno:'anything'}
#     '''
#     collection_name.delete_many(idno)
#     closeConnection(client)