from datetime import datetime

class User:
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