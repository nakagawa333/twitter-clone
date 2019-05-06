# -*- coding: utf-8 -*-
from PIL import Image
from flask import render_template, url_for, flash, redirect,request,abort
from Twitter import app,db,bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from Twitter.form import RegistrationForm,LoginForm,UpdateAccountForm,PostForm
from Twitter.models import User,Post

@app.route("/",methods=["GET","POST"])
@app.route("/home",methods=["GET","POST"])
@login_required
def home():
  form = PostForm()
  posts = Post.query.order_by(Post.date_posted.desc()).all()
  if request.method == "POST":
    post = Post(content=form.content.data,author=current_user)
    db.session.add(post)
    db.session.commit()
    return redirect("/home")
  return render_template("home.html",form=form,posts=posts)

@app.route("/register",methods=['GET','POST'])
def register():
  if current_user.is_authenticated:
    flash("あなたは、すでにログインしています。")
    return redirect(url_for('home'))
  form = RegistrationForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username=form.username.data,email=form.email.data,password=hashed_password)
    db.session.add(user)
    db.session.commit()
    flash('新たなアカウントの作成に成功しました')
    return redirect(url_for("login"))
  return render_template('register.html',title="Register",form=form)

@app.route("/login",methods=['GET','POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password,form.password.data):
      login_user(user,remember=form.remember.data)
      next_page = request.args.get('next')
      flash('あなたは、ログインに成功しました')
      return redirect(next_page) if next_page else redirect((url_for('home')))
    else:
      flash('あなたは、ログインに失敗しました。もう一度お願いします。')
  return render_template('login.html',title="Login",form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

def save_picture(form_picture):
  random_hex = secrests.token_hex(8)
  _,f_ext = os.path.splitext(form_picture.filename)
  picture_fn = random_hex + f_ext
  picture_path = os.path.join(app,root_path,'/',picture_fn)
  output_size = (125,125)
  i = Image.open(form_picture)
  i.save(picture_path)

  return picture_fn

@app.route("/account",methods=['GET','POST'])
@login_required
def account():
  form = UpdateAccountForm()
  if request.method == "POST":
    if form.picture.data:
      picture_file = save_picture(form.picture.data)
      current_user.image_file = picture_file
    current_user.username = form.username.data
    current_user.email = form.email.data
    db.session.commit()
    flash('Your account has been updated!', 'success')
    return redirect(url_for('account'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email
  image_file = url_for('static',filename = 'profile_pics/' + current_user.image_file)
  return render_template('account.html',title="Account",image_file=image_file,form=form)

if __name__ == "__main__":
  app.run(debug=True,port='9000', host='0.0.0.0')