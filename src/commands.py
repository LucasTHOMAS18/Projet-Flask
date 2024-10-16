from hashlib import sha256

import click
import yaml

from .app import app, db
from .models import Author, Book, User


@app.cli.command("load_db")
@click.argument("filename")
def load_bd(filename):
    """Creates the tables and populates them with data."""

    db.create_all()

    with open(filename) as file:
        books = yaml.load(file, Loader=yaml.Loader)

    authors = {}
    for book in books:
        author = book["author"]

        if author not in authors:
            author_instance = Author(name=author)
            db.session.add(author_instance)
            authors[author] = author_instance

    db.session.commit()

    for book in books:
        author_instance = authors[book["author"]]
        book_instance = Book(
            price=book["price"],
            title=book["title"],
            url=book["url"],
            img=book["img"],
            author_id=author_instance.id,
        )

        db.session.add(book_instance)

    db.session.commit()


@app.cli.command("new_user")
@click.argument("username")
@click.argument("password")
def new_user(username, password):
    """Adds a new user."""
    m = sha256()
    m.update(password.encode())
    u = User(username=username, password=m.hexdigest())
    db.session.add(u)
    db.session.commit()
