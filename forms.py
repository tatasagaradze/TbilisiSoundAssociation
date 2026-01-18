from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, DateField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, equal_to, Optional, ValidationError, Length

from models import User


class RegisterForms(FlaskForm):
    username = StringField("სახელი", validators=[DataRequired()] )
    email = StringField("იმეილი", validators=[DataRequired()] )
    password = PasswordField("პაროლი", validators = [DataRequired()])
    confirm_password = PasswordField("დაადასტურეთ პაროლი ხელმეორედ", validators =[DataRequired(), equal_to("password",  message="პაროლები უნდა ემთხვეოდეს")])
    submit = SubmitField("შექმნა", validators = [DataRequired()] )

    def validate_email(self, email):
        if '@' not in email.data:
            raise ValidationError('ელ.ფოსტა უნდა შეიცავდეს @ სიმბოლოს')

    def validate_password(self, password):
        if len(password.data) < 4:
            raise ValidationError('პაროლი უნდა შეიცავდეს მინიმუმ 4 სიმბოლოს')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('ეს სახელი უკვე გამოყენებულია')


class LoginForm(FlaskForm):
    username = StringField("შეიყვანე სახელი", validators=[DataRequired()] )
    password = PasswordField("შეიყვანე პაროლი", validators=[DataRequired()] )
    submit = SubmitField("შესვლა", validators = [DataRequired()] )

class ConcertForm(FlaskForm):

    img = FileField("ატვირთეთ ფოტო", validators=[FileRequired()] )#optional
    name = StringField("კონცერტის/სემინარის სახელი", validators=[DataRequired()] )
    datetime = DateField("თარიღი", validators = [DataRequired()] )
    info = TextAreaField("დამატებითი ინფორმაცია კონცერტის/სემინარის", validators=[DataRequired()] )
    submit= SubmitField("დაამატე", validators = [DataRequired()] )




class ArticleForm(FlaskForm):

    title = StringField("სტატიის სახელი", validators=[DataRequired()] )
    text = TextAreaField("აქ დაწერეთ -->", validators=[DataRequired()] )
    img = FileField("ატვირთეთ ფოტო სურვილის შემთხვევაში")
    submit = SubmitField("ატვირთვა", validators = [DataRequired()] )