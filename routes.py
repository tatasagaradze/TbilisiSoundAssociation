from datetime import datetime
from os import path
from flask import Flask, render_template, redirect, flash, request
from werkzeug.security import check_password_hash

from ext import app, db
from forms import ConcertForm, RegisterForms, ArticleForm, LoginForm
from models import Concert, User, Article
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegisterForms()

    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        new_user.create()
        login_user(new_user)
        return redirect("/")

    return render_template("signup.html", form=form)


@app.route("/")
def home():
    articles = Article.query.order_by(Article.created_at.desc()).all()
    users = User.query.all()

    return render_template("home.html", articles=articles, users=users, current_user=current_user)


@app.route("/create_concert", methods=["GET", "POST"])
@login_required
def create_concerts():
    #if not current_user.is_authenticated:
        #return redirect("/login")
    form = ConcertForm()
    if form.validate_on_submit():
        new_concert = Concert(name=form.name.data,
                              datetime=form.datetime.data,
                              info = form.info.data,
                              user_id=current_user.id,
                              img = form.img.data,
                              user_name=current_user.username)

        image = form.img.data
        print(image)
        directory = path.join(app.root_path, "static", "image", image.filename)
        image.save(directory)
        new_concert.img = image.filename

        new_concert.create()
        flash("კონცერტი/სესია წარმტებულად დაემატა")
        return redirect("/workshops")

    return render_template("create_concert.html", form=form)

@app.route("/create_article", methods=["GET", "POST"])
@login_required
def create_articles():
    if not current_user.is_authenticated:
        flash("ფუნქციის გამოსაყენებლად, სავალდებულოა დარეგისტრირება")
        return redirect("/login")
    form = ArticleForm()
    if form.validate_on_submit():
        new_article = Article(title=form.title.data,
                              text = form.text.data,
                              user_id=current_user.id,
                              img = form.img.data,
                              user_name=current_user.username,
                              created_at=datetime.now())
        if form.img.data is None: #tu ar aris rame atvirtuli
            new_article.img = None
        else:
            image = form.img.data
            directory = path.join(app.root_path, "static", "image", image.filename)
            image.save(directory)
            new_article.img = image.filename

        new_article.create()
        flash("სტატია წარმატებულად დაემატა")
        return redirect("/")
    return render_template("create_article.html", form=form)

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")


@app.route("/workshops")
def workshops():
    concerts = Concert.query.order_by(Concert.datetime.desc()).all()

    return render_template("workshops.html", concerts=concerts)


@app.route("/login", methods=["GET", "POST"])
def login():
    next_page = request.args.get('next')

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        print(user)
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("წარმატებული რეგისტრაცია")
            return redirect("/")
        else:
            flash("სახელი ან პაროლი არასწორია", "warning")

    if next_page:
        if '/create_concert' in next_page:
            flash("კონცერტის დასამატებლად გთხოვთ შეხვიდეთ სისტემაში", "warning")
        elif '/create_article' in next_page:
            flash("სტატიის დასამატებლად გთხოვთ შეხვიდეთ სისტემაში", "warning")
        elif '/profile' in next_page:
            flash("პროფილის სანახავად გთხოვთ შეხვიდეთ სისტემაში", "warning")
        else:
            flash("ამ გვერდის სანახავად გთხოვთ შეხვიდეთ სისტემაში", "warning")

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/update_concert/<int:concert_id>", methods=["GET", "POST"])
@login_required
def update_concert(concert_id):

    concert = Concert.query.get(concert_id)

    form = ConcertForm()

    if form.validate_on_submit():
        concert.name = form.name.data
        concert.datetime = form.datetime.data
        concert.info = form.info.data


        if form.img.data and form.img.data.filename:
            image = form.img.data
            directory = path.join(app.root_path, "static", "image", image.filename)
            image.save(directory)
            concert.img = image.filename

        concert.save()
        flash("კონცერტი წარმატებით განახლდა")
        return redirect('/workshops')


    form.name.data = concert.name
    form.datetime.data = concert.datetime
    form.info.data = concert.info

    return render_template("update_concert.html", concert=concert, form=form)


@app.route("/delete_concert/<int:concert_id>")
@login_required
def delete_concert(concert_id):
    concert = Concert.query.get(concert_id)
    if concert:
        concert.delete()
        flash("კონცერტი წარმატებით წაიშალა")

    return redirect("/workshops")

@app.route("/delete_article/<int:article_id>")
@login_required
def delete_article(article_id):

    article = Article.query.get(article_id)
    if article:
        article.delete()
        flash("სტატია წარმატებით წაიშალა")


    return redirect("/")


@app.route("/update_article/<int:article_id>", methods=["GET", "POST"])
@login_required
def update_article(article_id):

    article = Article.query.get(article_id)
    form = ArticleForm()

    if form.validate_on_submit():
        article.title = form.title.data
        article.text = form.text.data

        if form.img.data and form.img.data.filename:
            image = form.img.data
            directory = path.join(app.root_path, "static", "image", image.filename)
            image.save(directory)
            article.img = image.filename

        article.save()
        flash("სტატია წარმატებით განახლდა")
        return redirect("/")

    form.title.data = article.title
    form.text.data = article.text

    return render_template("update_article.html", article=article, form=form)


@app.route("/workshop_info/<int:concert_id>")
def workshop_info(concert_id):
    concert = Concert.query.filter(Concert.id == concert_id).first()
    user = User.query.get(concert.user_id) if concert else None
    return render_template("workshop_info.html", Concert=concert, User=user)

@app.route("/article_info/<int:article_id>")
def article_info(article_id):
    article = Article.query.get(article_id)
    user = User.query.get(article.user_id) if article else None
    return render_template("article_info.html", article=article, User=user)

@app.route("/profile")
@login_required
def profile():
    user_concerts = Concert.query.filter_by(user_id=current_user.id).all()

    user_articles = Article.query.filter_by(user_id=current_user.id).all()

    return render_template("profile.html", concerts=user_concerts, articles=user_articles, current_user=current_user)


