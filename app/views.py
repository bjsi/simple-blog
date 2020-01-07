from flask import current_app as app
from flask import render_template
from app import db
from app.models import Post


@app.route('/')
def index():
    posts = (db
             .session
             .query(Post)
             .all())
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/blog')
def blog():

    posts = (db
             .session
             .query(Post))

    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    posts.paginate()

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
