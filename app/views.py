from flask import current_app as app
from flask import render_template, request, url_for
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

    # Parse for pagination info
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 1, type=int), 100)

    posts = (db
             .session
             .query(Post)
             .paginate(page, per_page, False))

    prev_url = url_for('blog', page=posts.prev_num) \
               if posts.has_prev else None

    next_url = url_for('blog', page=posts.next_num) \
               if posts.has_next else None

    return render_template('blog.html',
                           posts=posts.items,
                           next_url=next_url,
                           prev_url=prev_url)


@app.route('/search')
def search():

    # Parse for pagination info
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 1, type=int), 100)

    # Parse for search info
    term = request.args.get('term')
    posts, total = Post.search(term, page, per_page)

    if term:
        next_url = url_for('search', term, page=page + 1) \
                   if total > page * per_page else None
        prev_url = url_for('search', term, page=page - 1) \
                   if page > per_page else None
        return render_template('blog.html', posts=posts,
                               next_url=next_url, prev_url=prev_url)
    else:
        redirect(url_for('blog'))


@app.route('/contact')
def contact():
    return render_template('contact.html')
