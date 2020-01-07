from app import db
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
    :summary: Text. A summary of the post.
    :content: Text. The post content.

    :tags: Relationship. Tags for the post.
    :author: Relationship. The author of the post.
    """

    __tablename__ = "posts"

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
    notes = db.relationship('Post',
                            secondary=post_tags,
                            back_populates='tags')

    def __init__(self, tag):
        self.tag = tag

    def __repr__(self):
        return f"<Tag id={self.id} tag={self.tag}>"
