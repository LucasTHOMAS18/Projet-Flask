import os.path

import yaml
from flask_login import UserMixin
from werkzeug.utils import secure_filename

from .app import db, login_manager
from .utils import mkpath


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    books = db.relationship("Book", back_populates="author")

    def __repr__(self):
        return f"Author{self.id, self.name}"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    url = db.Column(db.String(100))
    img = db.Column(db.String(100))
    price = db.Column(db.Float)

    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", back_populates="books")

    def __repr__(self):
        return f"Book{self.id, self.title}"


class User(db.Model, UserMixin):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(100))
    
    def get_id(self):
        return self.username


def get_sample(limit = 10) -> list[Book]:
    return Book.query.limit(limit).all()


def get_author(id: int) -> Author:
    return Author.query.get(id)


def get_author_by_name(name: str) -> Author | None:
    return Author.query.filter_by(name=name).first()


def update_author(id: int, name: int) -> Author:
    author = Author.query.get(id)
    
    if author:
        author.name = name
    else:
        author = Author(id=id, name=name)
        db.session.add(author)
    
    db.session.commit()
    return author


def get_book(id: int) -> Book:
    return Book.query.get(id)


def update_book(id: int, title: str, author_id: int, url: str, img, price: float) -> Book:
    book = Book.query.get(id)
    
    if book:
        book.title = title
        book.author_id = author_id
        book.url = url
        book.price = price
        if img:
            # Code pour gérer l'upload de l'image (exemple)
            filename = secure_filename(img.filename)
            img.save(os.path.join('src/static/images', filename))
            book.img = filename
    else:
        book = Book(title=title, author_id=author_id, url=url, img=img.filename, price=price)
        db.session.add(book)
    
    db.session.commit()
    return book


@login_manager.user_loader
def load_user(username):
    return User.query.get(username)
