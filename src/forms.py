from hashlib import sha256

from flask_wtf import FlaskForm
from wtforms import HiddenField, IntegerField, PasswordField, StringField, TextAreaField
from wtforms.validators import DataRequired, NumberRange

from .models import Author, Book, User


class AuthorForm(FlaskForm):
    id = HiddenField("id")
    name = StringField("Nom", validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    next = HiddenField()
    
    def get_authenticated_user(self):
        user = User.query.get(self.username.data)
        
        if user is None:
            return None
        
        m = sha256()
        m. update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None


class CommentForm(FlaskForm):
    rating = IntegerField('Votre note (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    content = TextAreaField('Votre commentaire', validators=[DataRequired()])
