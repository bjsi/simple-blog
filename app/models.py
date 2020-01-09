from app import db
import re
import datetime as dt


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


class Post(db.Model):

    """ Post Model
    :id: Integer. Unique post id
    :created_at: DateTime. UTC datetime
    :title: Text. Title of the post.
    :slug: Text. URL representation of the title.
    :published: Boolean. True if visible on the site.
    :summary: Text. A summary of the post.
    :content: Text. The post content.

    :tags: Relationship. Tags for the post.
    """

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow())
    title = db.Column(db.Text, nullable=False)
    slug = db.Column(db.Text, unique=True)
    published = db.Column(db.Boolean, default=0)
    summary = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)

    # Posts >-< Tags
    tags = db.relationship("Tag",
                           secondary=post_tags,
                           back_populates='posts')

    @classmethod
    def public(cls):
        query = (db
                 .session
                 .query(Post)
                 .filter(Post.published.is_(True)))
        return query

    def save(self):
        if not self.slug:
            self.slug = re.sub('[^\w]+', '-', self.title.lower())
        db.session.add(self)
        db.session.commit()

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
