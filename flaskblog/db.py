from pymongo import MongoClient
from bson.objectid import ObjectId


def register_user(User):
    data = {
        'username': User.username,
        'email': User.email,
        'password': User.password,
        'posts': User.posts,
        'image_file': User.image_file
    }
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


def updatePassword(old, new):
    new = {'$set': new}
    user_collection.update_one(old, new)


def newPost(Post):
    data = {
        'title': Post.title,
        'date_posted': Post.date_posted,
        'content': Post.content,
        'author': Post.author,
        'email': Post.email,
        'image_file': Post.image_file,
        'user_id': Post.user_id
    }
    return post_collection.insert_one(data)


def fetchPosts(page, total_cards):
    skip_val = (page - 1) * total_cards
    posts = post_collection.find().sort("_id", -1).skip(skip_val).limit(5)
    return posts


def fetchUserPosts(username, page, total_cards):
    try:
        skip_val = (page - 1) * total_cards
        return post_collection.find({
            'author': username
        }).sort("_id", -1).skip(skip_val).limit(5)
    except:
        return False


def getPost(post_id):
    try:
        return post_collection.find_one({'_id': ObjectId(post_id)})
    except:
        return False


def updatePost(post_id, updated_post):
    old = {'_id': ObjectId(post_id)}
    new = {'$set': updated_post}
    post_collection.update_one(old, new)


def deletePost(post_id):
    post_collection.delete_one({'_id': ObjectId(post_id)})


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