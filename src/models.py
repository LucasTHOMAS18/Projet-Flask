import os.path

import yaml
from flask_login import UserMixin
from datetime import datetime

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


class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # Rating between 1 to 5

    user = db.relationship('User', backref='user_ratings')
    book = db.relationship('Book', backref='book_ratings')


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # Note entre 1 et 5
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='comments')
    book = db.relationship('Book', backref='comments')


def get_average_rating(book_id: int):
    ratings = Rating.query.filter_by(book_id=book_id).all()
    comments = Comment.query.filter_by(book_id=book_id).all()
    
    all_ratings = [r.rating for r in ratings] + [c.rating for c in comments]
    
    if not all_ratings:
        return 0
    
    total = sum(all_ratings)
    return total / len(all_ratings)

def get_user_rating(book_id: int, user_id: str):
    comment = Comment.query.filter_by(book_id=book_id, user_id=user_id).first()
    return comment.rating if comment else None


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
