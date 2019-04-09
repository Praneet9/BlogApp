from flask import Flask, render_template

app = Flask(__name__)

posts = [
    {
        'author': 'Praneet Bomma',
        'title': 'First Post',
        'date_posted': 'April 8, 2019',
        'content': 'This is my first post'
    },
    {
        'author': 'Jane Doe',
        'title': 'Second Post',
        'date_posted': 'April 9, 2019',
        'content': 'This is the second post'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts = posts)

@app.route('/about')
def about():
    return render_template('about.html', title = 'About')

if __name__ == '__main__':
    app.run(debug=True)