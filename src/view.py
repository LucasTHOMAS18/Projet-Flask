from flask import redirect, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField
from wtforms.validators import DataRequired

from .app import app, db
from .models import Author, Book, get_author, get_book, get_sample, book_by_author


class AuthorForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Nom', validators=[DataRequired()])
   

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
def edit_author(id):
    author = get_author(id)
    form = AuthorForm(id=author.id, name=author.name)
    return render_template("edit-author.html", author=author, form=form)


@app.route("/add/author")
def add_author():
    form = AuthorForm()
    return render_template("add-author.html", form=form)


@app.route("/add/author", methods=["POST"])
def create_author():
    author = None
    form = AuthorForm() 
    
    if form.validate_on_submit():
        author = Author(name=form.name.data)
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('detail_author', id=author.id)) 
    
    author = get_author((int(form.id.data)))
    return render_template("add-author.html", form=form)


@app.route("/save/author", methods=["POST"])
def save_author():
    author = None
    form = AuthorForm()
    
    if form.validate_on_submit():
        id = int(form.id.data)
        author = get_author(id)
        author.name = form.name.data
        db.session.commit()
        return redirect(url_for('detail_author', id=author.id))
    
    author = get_author((int(form.id.data)))
    return render_template("edit-author.html", author=author, form=form)

@app.route("/search")
def search_bar():
    search_query = request.args.get('q', '')
    books = book_by_author(search_query)
    return render_template("search.html", title=f"Search results for '{search_query}'", books=books)

