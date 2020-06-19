from . import db
class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(30),nullable=False,unique=True)
    email=db.Column(db.String(50))
    password_hash=db.Column(db.String)
    category=db.Column(db.String)
    profile_pic_path=db.Column(db.String,default='profile.png')
    bio=db.Column(db.String)
    blog=db.relationship('Blogs',backref='user',lazy='dynamic')
    comment=db.relationship('Comment',backref='user',lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('Permission not allowed!')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"User {self.username}"


date_time=datetime.utcnow().replace(tzinfo=pytz.UTC)
time_zone=date_time.astimezone(pytz.timezone('Africa/Nairobi'))
class Blogs(db.Model):
    __tablename__="blogs"
    id=db.Column(db.Integer,primary_key=True)
    blog=db.Column(db.String,nullable=False)
    category=db.Column(db.String)
    posted_date=db.Column(db.DateTime,default=time_zone)
    upvotes=db.Column(db.Integer)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    comment=db.relationship('Comment',backref='blogs',lazy='dynamic')

    def save_blog(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_blogs(cls,user_id):
        blog=Blogs.query.filter_by(user_id=user_id).all()
        return blog

class  Comment(db.Model):
    __tablename__="comments"
    id=db.Column(db.Integer,primary_key=True)
    comment=db.Column(db.String)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    blog_id=db.Column(db.Integer,db.ForeignKey('blogs.id'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_comment(cls,blog_id):
        comment=Comment.query.filter_by(blog_id=blog_id).all()
        return comment