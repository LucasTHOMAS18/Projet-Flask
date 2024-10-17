from flask import redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user

from .app import app, db
from .forms import AuthorForm, LoginForm, RatingForm
from .models import get_author, get_book, get_sample, update_author, Rating, get_average_rating, get_user_rating


@app.route("/")
def home():
    return render_template("home.html", title="My Books !", books = get_sample(10))


@app.route("/books/<int:id>", methods=["GET"])
def detail_book(id):
    book = get_book(id)
    user_rating = None
    average_rating = get_average_rating(id)
    form = RatingForm()  # Instancie le formulaire de notation

    if current_user.is_authenticated:
        user_rating = get_user_rating(book.id, current_user.username)

    return render_template("book.html", book=book, form=form, user_rating=user_rating, average_rating=average_rating)


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

# Ajoute un livre en favoris
@app.route('/favorite/<int:book_id>', methods=['POST'])
@login_required
def add_favorite(book_id):
    book = get_book(book_id)
    if book not in current_user.favorite_books:
        current_user.favorite_books.append(book)
        db.session.commit()
    return redirect(url_for('detail_book', id=book_id))


# Retire un livre des favoris
@app.route('/unfavorite/<int:book_id>', methods=['POST'])
@login_required
def remove_favorite(book_id):
    book = get_book(book_id)
    if book in current_user.favorite_books:
        current_user.favorite_books.remove(book)
        db.session.commit()
    return redirect(url_for('detail_book', id=book_id))


# Liste des favoris
@app.route('/favorites')
@login_required
def view_favorites():
    return render_template('favorites.html', books=current_user.favorite_books)


# System notation
@app.route("/rate/<int:book_id>", methods=["POST"])
@login_required
def rate_book(book_id):
    form = RatingForm()

    if form.validate_on_submit():
        rating = Rating.query.filter_by(book_id=book_id, user_id=current_user.username).first()
        if rating:
            rating.rating = form.rating.data  # Update the existing rating
        else:   
            new_rating = Rating(user_id=current_user.username, book_id=book_id, rating=form.rating.data)
            db.session.add(new_rating)
        db.session.commit()
        return redirect(url_for('detail_book', id=book_id))
    return redirect(url_for('detail_book', id=book_id))
