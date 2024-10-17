import os.path

import yaml
from flask_login import UserMixin

from .app import db, login_manager
from .utils import mkpath

favorites = db.Table(
    'favorites',
    db.Column('user_id', db.String(50), db.ForeignKey('user.username'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
)

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
    
    favorite_books = db.relationship('Book', secondary=favorites, backref='favorited_by')

    
    def get_id(self):
        return self.username


def get_sample(limit = 10) -> list[Book]:
    return Book.query.limit(limit).all()


def get_author(id: int) -> Author:
    return Author.query.get(id)


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


@login_manager.user_loader
def load_user(username):
    return User.query.get(username)
