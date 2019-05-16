from django.shortcuts import render

posts = [
    {
        'author': 'Praneet',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'May 15, 2019'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'May 16, 2019'
    }
]

def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})