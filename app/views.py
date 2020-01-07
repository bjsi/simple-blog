from flask import current_app as app
from flask import render_template
from app import db
from app.models import Post


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/blog')
def blog():
    posts = (db
             .session
             .query(Post)
             .all())

    return render_template('blog.html', posts=posts)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/tags', methods=['POST'])
def tags():
    return render_template('search_results.html')


@app.route('/search', methods=['POST'])
def search():
    return render_template('search_results.html')
