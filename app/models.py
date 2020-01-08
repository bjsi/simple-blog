from app import db
import datetime as dt
from app.search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


post_tags = db.Table("post_tags",
                     db.Column('posts_id',
                               db.Integer,
                               db.ForeignKey('posts.id'),
                               primary_key=True,
                               nullable=False),
                     db.Column("tag_id",
                               db.Integer,
                               db.ForeignKey('tags.id'),
                               primary_key=True,
                               nullable=False))


class Post(SearchableMixin, db.Model):

    """ Post Model
    :id: Integer. Unique post id
    :created_at: DateTime. UTC datetime
    :title: Text. Title of the post.
    :summary: Text. A summary of the post.
    :content: Text. The post content.

    :tags: Relationship. Tags for the post.
    :author: Relationship. The author of the post.
    """

    __tablename__ = "posts"
    __searchable__ = ['title', 'summary', 'content']

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow())
    title = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)

    # Posts >-< Tags
    tags = db.relationship("Tag",
                           secondary=post_tags,
                           back_populates='posts')

    # author = db.relationship('Author')

    def __repr__(self):
        return f"<Post id={self.id} title={self.title}>"


class Tag(db.Model):

    """ Tag Model
    :id: Integer. Unique tag id.
    :tag: Text. The text for the tag.
    :posts: Relationship. Posts with this tag
    """

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.Text, nullable=False)
    posts = db.relationship('Post',
                            secondary=post_tags,
                            back_populates='tags')

    def __init__(self, tag):
        self.tag = tag

    def __repr__(self):
        return f"<Tag id={self.id} tag={self.tag}>"
