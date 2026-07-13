from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from hashlib import md5
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
import os
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")
ckeditor = CKEditor(app)
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI")
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(250))
    password: Mapped[str] = mapped_column(String(100))
    posts: Mapped["BlogPost"] = relationship(back_populates="author")
    comments: Mapped["Comment"] = relationship(back_populates="author")

    def avatar(self, size=100):
        email = self.email.strip().lower()
        email_hash = md5(email.encode()).hexdigest()
        default = "" if self.id == 1 else "&d=identicon"
        return f"https://www.gravatar.com/avatar/{email_hash}?s={size}{default}"

class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped["User"] = relationship(back_populates="posts")
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    comments: Mapped["Comment"] = relationship(back_populates="parent_post")

class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(250), nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="comments")
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("blog_posts.id"))
    parent_post: Mapped["BlogPost"] = relationship(back_populates="comments")

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_only(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.id == 1:
                return function(*args, **kwargs)
            else:
                abort(403)
        else:
            return redirect(url_for("login"))
    return wrapper

@app.route('/register', methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        hashed_password = generate_password_hash(password=register_form.password.data,
                                                 salt_length=8)
        new_user = User(
            name=register_form.name.data,
            email=register_form.email.data,
            password=hashed_password
        )
        if db.session.execute(db.select(User).where(User.email == register_form.email.data)).scalar():
            flash(message="That email already exists, Log In instead!")
            return redirect(url_for("login"))
        else:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("get_all_posts"))

    return render_template("register.html", form=register_form, user=current_user)

@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == login_form.email.data)).scalar()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for("login"))

        if check_password_hash(user.password, login_form.password.data):
            login_user(user)
            return redirect(url_for("get_all_posts"))
        else:
            flash(message="Password incorrect, please try again.")
            return redirect(url_for("login"))
    return render_template("login.html", form=login_form, user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts, user=current_user)

@app.route("/post/<int:post_id>", methods=["GET", "POST"])
@login_required
def show_post(post_id):
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        if current_user.is_authenticated:
            comment = comment_form.comment.data
            new_comment = Comment(
                text=comment,
                author_id=current_user.id,
                post_id=post_id
            )
            db.session.add(new_comment)
            db.session.commit()
        else:
            flash(message="You need to login or register to comment.")
            return redirect(url_for("login"))

    requested_post = db.get_or_404(BlogPost, post_id)
    comments_for_post = db.session.execute(db.select(Comment).where(Comment.post_id == post_id)).scalars().all()
    return render_template("post.html", post=requested_post, user=current_user, form=comment_form,
                           comments=comments_for_post)

@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, user=current_user)

@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True, user=current_user)

@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html", user=current_user)


@app.route("/contact")
def contact():
    return render_template("contact.html", user=current_user)


if __name__ == "__main__":
    app.run(debug=False, port=5002)
