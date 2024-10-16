from flask import redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from .app import app, db
from .forms import AuthorForm, LoginForm
from .models import Author, get_author, get_book, get_sample, update_author


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
    
    if form.validate_on_submit():
        author_id = int(form.id.data) if form.id.data else None
        author = update_author(author_id, form.name.data)
        
        return redirect(url_for('detail_author', id=author.id))
    
    author_id = int(form.id.data) if form.id.data else None
    author = update_author(author_id, form.name.data)
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
