from hashlib import sha256

from flask_wtf import FlaskForm
from wtforms import HiddenField, PasswordField, StringField
from wtforms.validators import DataRequired

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
