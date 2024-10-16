import os.path

import yaml

from .app import db
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
    
    author_id =  db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", back_populates="books")
    
    def __repr__(self):
        return f"Book{self.id, self.title}"


def get_sample() -> list[Book]:
    return Book.query.limit(10).all()


def get_author(id: int) -> Author:
    return Author.query.get(id)


def get_book(id: int) -> Book:
    return Book.query.get(id)


def book_by_author(search: str) -> list[Book]:
    return Book.query.join(Author).filter(Author.name.ilike(f'{search}%')).all()



