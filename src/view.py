from flask import render_template

from .app import app, db
from .models import Author, Book, get_sample


@app.route("/")
def home():
    return render_template(
        "home.html",
        title="My Books !",
        books = get_sample()
    )
    
@app.route("/detail/<id>")
def detail(id):
    book = db.session.get(Book, {"id": id})
    return render_template("detail.html", book=book)
