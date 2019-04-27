from datetime import datetime
from flaskblog import login_manager
from flaskblog.db import get_user
from flask_login import UserMixin, current_user



@login_manager.user_loader
def load_user(user_id):
    user = get_user(user_id)
    user['is_authenticated'] = True
    return User_Model(user)

class User():
    def __init__(self, username, email, password, image_file = 'default.jpg', posts = None):
        self.username = username
        self.email = email
        self.image_file = image_file
        self.password = password
        self.posts = posts

class Post:
    def __init__(self, title, content, user_id, date_posted = datetime.utcnow):
        self.title = title
        self.date_posted = date_posted
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return "Post('"+self.title+"', '"+self.date_posted+"')"


class User_Model():
    def __init__(self, user):
        # UserMixin.__setattr__('is_authenticated', True)
        self.username = user['username']
        self.id = str(user['_id'])
        try:
            self.is_authenticated = user['is_authenticated']
            self.is_active = True
            # self.is_anonymouse = False
        except:
            self.is_authenticated = False
            self.is_active = False
            # self.is_authenticated = True
    
    def get_id(self):
        return self.id