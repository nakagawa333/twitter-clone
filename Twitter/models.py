from datetime import datetime
from Twitter import app,login_manager,db
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))


class User(db.Model,UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
  password = db.Column(db.String(60), nullable=False)
  posts = db.relationship('Post', backref='author', lazy=True)

  def __repr__(self):
    return "User(username={0},email={1},image_file={2})".format(self.username,self.email,self.image_file)

class Post(db.Model):
  id = db.Column(db.Integer,primary_key=True)
  content = db.Column(db.Text,nullable=False)
  date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
  user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

  def __repr__(self):
    return "Post(id={0},content={1},user_id={2},date_posted={3})".format(self.id,self.content,self.user_id,self.date_posted)
    