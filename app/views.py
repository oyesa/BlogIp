from flask import render_template
from app import app


#views
@app.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Welcome to THA TECH STREETS Blog'
    return render_template('index.html', title = title)

@app.route('/blog/<blog_id>')
def blog(blog_id):

    '''
    View movie page function that returns the movie details page and its data
    '''
    return render_template('blog.html',id = blog_id)