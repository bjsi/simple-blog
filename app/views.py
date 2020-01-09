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
    per_page = min(request.args.get('per_page', 5, type=int), 100)

    posts = Post.public().paginate(page, per_page, False)

    prev_url = url_for('blog', page=posts.prev_num) \
               if posts.has_prev else None

    next_url = url_for('blog', page=posts.next_num) \
               if posts.has_next else None

    return render_template('blog.html',
                           posts=posts.items,
                           next_url=next_url,
                           prev_url=prev_url)


@app.route('/<slug>')
def detail(slug):
    post = (db
            .session
            .query(Post)
            .filter(Post.slug.is_(slug))
            .one_or_none())
    if post:
        return render_template('post.html', post=post)
    else:
        return render_template('404.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')
