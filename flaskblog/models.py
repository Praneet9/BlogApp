from datetime import datetime
from flaskblog import login_manager, app
from flaskblog.db import get_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin, current_user


@login_manager.user_loader
def load_user(user_id):
    user = get_user(user_id)
    user['is_authenticated'] = True
    return User_Model(user)


class User():
    def __init__(self,
                 username,
                 email,
                 password,
                 image_file='default.jpg',
                 posts=None):
        self.username = username
        self.email = email
        self.image_file = image_file
        self.password = password
        self.posts = posts


class Post:
    def __init__(self,
                 title,
                 content,
                 date_posted=datetime.utcnow().strftime('%Y-%m-%d')):
        self.title = title
        self.date_posted = date_posted
        self.content = content
        self.author = current_user.username
        self.image_file = current_user.image_file
        self.email = current_user.email
        self.user_id = current_user.id

    def __repr__(self):
        return "Post('" + self.title + "', '" + self.date_posted + "')"


class User_Model():
    def __init__(self, user):
        # UserMixin.__setattr__('is_authenticated', True)
        self.username = user['username']
        self.id = str(user['_id'])
        self.email = user['email']
        self.image_file = user['image_file']
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymouse = False

    def get_id(self):
        return self.id

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        user = get_user(user_id)
        user['is_authenticated'] = True
        return User_Model(user)