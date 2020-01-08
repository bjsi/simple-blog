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
    """ TODO: Add search """

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


@app.route('/contact')
def contact():
    return render_template('contact.html')
