from flask import render_template, abort, redirect, request, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from app import db
from app.main.forms import NewsForm, MyProfile, GetPrivelegy, CommentsCreateForm
from app.models import User, Articles, Comment
from app.main import bp


@bp.route("/")
@bp.route("/index")
def index():
    article = Articles.query.order_by(Articles.id.desc()).limit(4).all()[::-1]
    return render_template("index.html", articles=article)


# games
@bp.route('/games')
def games():
    article = db.session.query(Articles).filter(Articles.category == 1)[::-1]
    return render_template("forms/games_form.html", articles=article)


# movies
@bp.route('/movies')
def movies():
    article = db.session.query(Articles).filter(Articles.category == 2)[::-1]
    return render_template("forms/movies_form.html", articles=article)


# series
@bp.route('/series')
def series():
    article = db.session.query(Articles).filter(Articles.category == 3)[::-1]
    return render_template("forms/series_form.html", articles=article)


# books
@bp.route('/books')
def books():
    article = db.session.query(Articles).filter(Articles.category == 4)[::-1]
    return render_template("forms/books_form.html", articles=article)


@bp.route('/article/<int:id>', methods=['GET', 'POST'])
def article(id):
    comment_form = CommentsCreateForm()
    article = db.session.query(Articles).filter(Articles.id == id).first()
    creator = db.session.query(User).filter(User.id == article.creator).first()
    comments = db.session.query(Comment).filter(Comment.article_id == id).all()  # список кометариев
    if comment_form.validate_on_submit():
        comment = Comment()
        comment.comment_creator = current_user.id
        comment.article_id = id
        comment.content = comment_form.text.data

        current_user.comment.append(comment)
        db.session.commit()
        return render_template("news_template.html", article=article, creator=creator, comments=comments,
                               form=comment_form)
    return render_template("news_template.html", article=article, creator=creator, comments=comments, form=comment_form)


@bp.route("/create_news", methods=['GET', 'POST'])
@login_required
def create_news():
    if current_user:
        form = NewsForm()
        if form.validate_on_submit():
            article = Articles()
            article.title = form.title.data
            article.heading = form.heading.data
            article.content = form.content.data
            article.category = form.category.data[0]
            article.likes = 0
            article.dislikes = 0

            if request.files["file"]:
                file = request.files["file"]
                article.image = current_user.username + secure_filename(file.filename)
                f = open(current_app.config['UPLOAD_FOLDER'] + current_user.username + file.filename, 'wb')
                f.write(file.read())
                f.close()
            else:
                article.image = "nophoto.jpg"

            current_user.article.append(article)
            db.session.merge(current_user)
            db.session.commit()
            return redirect('/')
        return render_template('news_create.html', title='Добавление новости', form=form)


@bp.route("/my_news", methods=['GET', 'POST'])
@login_required
def my_news():
    article = db.session.query(Articles).filter(Articles.creator == current_user.id)
    return render_template("my_news.html", title='Мои новости', articles=article)


@bp.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    article = db.session.query(Articles).filter(Articles.id == id).first()
    if article:
        db.session.delete(article)
        db.session.commit()
    else:
        abort(404)
    return redirect('/')


@bp.route('/news_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        article = db.session.query(Articles).filter(Articles.id == id).first()

        if article:
            form.title.data = article.title
            form.heading.data = article.heading
            form.content.data = article.content
            form.category.default = [article.category]
        else:
            abort(404)
    if form.validate_on_submit():
        article = db.session.query(Articles).filter(Articles.id == id).first()

        if article:
            article.title = form.title.data
            article.heading = form.heading.data
            article.content = form.content.data
            article.content += " (статья изменена)"
            article.category = form.category.data

            file = request.files["file"]
            article.image = current_user.username + secure_filename(file.filename)
            f = open(current_app.config['UPLOAD_FOLDER'] + current_user.username + file.filename, 'wb')
            f.write(file.read())
            f.close()

            db.session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news_create.html', title='Редактирование новости', form=form)


@bp.route('/my_profile', methods=['GET', 'POST'])
@login_required
def my_profile():
    form = MyProfile()
    if request.method == "GET":
        user = db.session.query(User).filter(User.id == current_user.id).first()
        if user:
            form.username.data = user.username
            form.email.data = user.email
            if user.position == 1:
                form.position.data = "Писатель"
            else:
                form.position.data = "Читатель"
        else:
            abort(404)
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.id == current_user.id).first()
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        return redirect("/")
    return render_template('my_profile.html', title='мой профиль', form=form, user=user)


# Получение возможности создать новость
@bp.route('/get_poster', methods=['GET', 'POST'])
@login_required
def get_poster():
    form = GetPrivelegy()
    if form.validate_on_submit():
        if form.text.data == "Супер-пупер_секрeтный_код":
            current_user.position = 1
            db.session.commit()
            return redirect("/")
        else:
            return render_template('get_poster.html', message="Неправильный код", form=form)
    return render_template('get_poster.html', title='Получить привелегию', form=form)


@bp.route('/user/<int:id>', methods=['GET', 'POST'])
def curent_user_profile(id):
    pass