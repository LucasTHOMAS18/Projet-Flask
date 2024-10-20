from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from .app import app, db
from .forms import AuthorForm, CommentForm, LoginForm
from .models import (Comment, Rating, get_author, get_average_rating, get_book,
                     get_book_amount, get_sample, get_user_rating,
                     search_books, update_author)


@app.route("/")
@app.route("/<int:page>")
def home(page = 1):
    return render_template("home.html", title="My Books !", books = get_sample(10, (page - 1) * 10), pages=range(1, (get_book_amount() // 10) + 1))


@app.route("/books/<int:id>", methods=["GET", "POST"])
def detail_book(id):
    book = get_book(id)
    form = CommentForm()
    comments = get_comments(id)
    
    if form.validate_on_submit():
        if process_comment_form(form, id):
            # Redirection après soumission pour éviter le double envoi
            return redirect(url_for('detail_book', id=id))

    user_rating = get_user_rating_for_book(book.id)
    average_rating = get_average_rating(book.id)

    return render_template("book.html", book=book, user_rating=user_rating, average_rating=average_rating, form=form, comments=comments)



def get_comments(book_id):
    return Comment.query.filter_by(book_id=book_id).order_by(Comment.timestamp.desc()).all()


def process_comment_form(form, book_id):
    existing_comment = Comment.query.filter_by(user_id=current_user.username, book_id=book_id).first()
    
    if form.validate_on_submit():
        if existing_comment:
            existing_comment.content = form.content.data
            existing_comment.rating = form.rating.data
            flash("Votre commentaire et votre note ont été mis à jour.", "info")
        else:
            new_comment = Comment(
                user_id=current_user.username,
                book_id=book_id,
                content=form.content.data,
                rating=form.rating.data
            )
            db.session.add(new_comment)
            flash("Votre commentaire a été ajouté.", "success")

        db.session.commit()

        # Redirige pour éviter une nouvelle soumission avec le bouton de retour en arrière
        return True

    return False



def get_user_rating_for_book(book_id):
    return get_user_rating(book_id, current_user.username) if current_user.is_authenticated else None


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


@app.route('/favorite/<int:book_id>', methods=['POST'])
@login_required
def add_favorite(book_id):
    book = get_book(book_id)
    if book not in current_user.favorite_books:
        current_user.favorite_books.append(book)
        db.session.commit()
    
    next_url = request.args.get('next', url_for('detail_book', id=book_id))
    return redirect(next_url)


@app.route('/unfavorite/<int:book_id>', methods=['POST'])
@login_required
def remove_favorite(book_id):
    book = get_book(book_id)
    if book in current_user.favorite_books:
        current_user.favorite_books.remove(book)
        db.session.commit()
        
    next_url = request.args.get('next', url_for('detail_book', id=book_id))
    return redirect(next_url)


@app.route('/favorites')
@login_required
def view_favorites():
    return render_template('favorites.html', books=current_user.favorite_books)


@app.route("/rate/<int:book_id>", methods=["POST"])
@login_required
def rate_book(book_id):
    rating = Rating.query.filter_by(book_id=book_id, user_id=current_user.username).first()
    
    if rating:
        rating.rating = request.form.get('rating', type=int)
    else:   
        new_rating = Rating(user_id=current_user.username, book_id=book_id, rating=request.form.get('rating', type=int))
        db.session.add(new_rating)
    
    db.session.commit()
    
    return redirect(url_for('detail_book', id=book_id))

# Systeme de recherche
@app.route("/search", methods=["get"])
def search():
    query = request.args.get("search")
    search_by = request.args.get("search_by", "title")
    order_by = request.args.get("order_by", "alpha")
    
    res = search_books(query, search_by, order_by)
    return render_template('search.html', books=res)