from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from .app import app, db
from .forms import AuthorForm, BookForm, LoginForm
from .models import (get_author, get_author_by_name, get_book, get_sample,
                     update_author, update_book)


@app.route("/")
def home():
    return render_template("home.html", title="My Books !", books = get_sample(50))


@app.route("/books/<id>")
def detail_book(id):
    book = get_book(id)
    return render_template("book.html", book=book)


@app.route("/authors/<id>")
def detail_author(id):
    author = get_author(id)
    return render_template("author.html", author=author)


@app.route("/add/author", methods=["POST", "GET"])
@app.route("/edit/author/<int:id>", methods=["POST", "GET"])
@login_required
def save_author(id: int | None = None):
    author = get_author(id)
    form = AuthorForm(id=author.id, name=author.name) if author else AuthorForm()
    
    author_id = int(form.id.data) if form.id.data else None
    
    if form.validate_on_submit():
        author = update_author(author_id, form.name.data)
        return redirect(url_for('detail_author', id=author.id))
    
    return render_template("edit-author.html", form=form)


@app.route("/add/book", methods=["POST", "GET"])
@app.route("/edit/book/<int:id>", methods=["POST", "GET"])
@login_required
def save_book(id: int | None = None):
    book = get_book(id)
    form = BookForm(id=book.id, name=book.title, author=book.author.name, url=book.url, prix=book.price) if book else BookForm()
    
    if form.validate_on_submit():
        book_id = int(form.id.data) if form.id.data else None
        author = get_author_by_name(form.author.data)
        if not author:
            return render_template("edit-book.html", book=book, form=form)

        book = update_book(book_id, form.name.data, author.id, form.url.data, form.img.data, form.prix.data)
        return redirect(url_for('detail_book', id=book.id))

    return render_template("edit-book.html", book=book, form=form)


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
