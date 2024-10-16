from hashlib import sha256

from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import HiddenField, PasswordField, StringField
from wtforms.validators import DataRequired

from .app import app, db
from .models import Author, Book, User, get_author, get_book, get_sample


# Forms
class AuthorForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Nom', validators=[DataRequired()])
   

class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    next = HiddenField()
    
    def get_authenticated_user(self):
        user = User.query.get(self.username.data)
        
        if user is None:
            return None
        
        m = sha256()
        m. update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None


# Routes
@app.route("/")
def home():
    return render_template(
        "home.html",
        title="My Books !",
        books = get_sample()
    )


@app.route("/books/<id>")
def detail_book(id):
    book = get_book(id)
    return render_template("book.html", book=book)


@app.route("/authors/<id>")
def detail_author(id):
    author = get_author(id)
    return render_template("author.html", author=author)


@app.route("/edit/author/<int:id>")
@login_required
def edit_author(id):
    author = get_author(id)
    form = AuthorForm(id=author.id, name=author.name)
    return render_template("edit-author.html", author=author, form=form)


@app.route("/add/author")
@login_required
def add_author():
    form = AuthorForm()
    return render_template("add-author.html", form=form)


@app.route("/add/author", methods=["POST"])
@login_required
def create_author():
    author = None
    form = AuthorForm()
    
    if form.validate_on_submit():
        author = Author(name=form.name.data)
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('detail_author', id=author.id)) 
    
    return render_template("add-author.html", form=form)


@app.route("/save/author", methods=["POST"])
@login_required
def save_author():
    author = None
    form = AuthorForm()
    
    if form.validate_on_submit():
        id_author = int(form.id.data)
        author = get_author(id_author)
        author.name = form.name.data
        db.session.commit()
        return redirect(url_for('detail_author', id=author.id))
    
    author = get_author((int(form.id.data)))
    return render_template("edit-author.html", author=author, form=form)


@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    
    if not form.is_submitted():
        form.next.data = request.args.get("next")

    if form.validate_on_submit():
        user = form.get_authenticated_user()
        
        if user:
            login_user(user)
            return redirect(form.next.data if form.next.data != "" else url_for("home"))
    
    return render_template("login.html", form=form)


@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("home"))
