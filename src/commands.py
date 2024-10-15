import click
import yaml

from .app import app, db
from .models import Author, Book


@app.cli.command('load_db')
@click.argument('filename')
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
            price = book["price"],
            title = book["title"],
            url = book["url"] ,
            img = book["img"] ,
            author_id = author_instance.id
            )
        
        db.session.add(book_instance)
        
    db.session.commit()
