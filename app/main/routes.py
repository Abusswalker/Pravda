from flask import render_template, abort, redirect, request, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from app import db
from app.main.forms import NewsForm, MyProfile, GetPrivelegy
from app.models import User, Articles
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
    return render_template("games_form.html", articles=article)


@bp.route('/games/<int:id>', methods=['GET', 'POST'])
def games_news(id):
    article = db.session.query(Articles).filter(Articles.id == id).first()
    creator = db.session.query(User).filter(User.id == article.creator).first()
    return render_template("news_template.html", article=article, creator=creator)


# movies
@bp.route('/movies')
def movies():
    article = db.session.query(Articles).filter(Articles.category == 2)[::-1]
    return render_template("movies_form.html", articles=article)


@bp.route('/movies/<int:id>', methods=['GET', 'POST'])
def movies_news(id):
    article = db.session.query(Articles).filter(Articles.id == id).first()
    creator = db.session.query(User).filter(User.id == article.creator).first()
    return render_template("news_template.html", article=article, creator=creator)


# series
@bp.route('/series')
def series():
    article = db.session.query(Articles).filter(Articles.category == 3)[::-1]
    return render_template("series_form.html", articles=article)


@bp.route('/series/<int:id>', methods=['GET', 'POST'])
def series_news(id):
    article = db.session.query(Articles).filter(Articles.id == id).first()
    creator = db.session.query(User).filter(User.id == article.creator).first()
    return render_template("news_template.html", article=article, creator=creator)


# books
@bp.route('/books')
def books():
    article = db.session.query(Articles).filter(Articles.category == 4)[::-1]
    return render_template("books_form.html", articles=article)


@bp.route('/books/<int:id>', methods=['GET', 'POST'])
def books_news(id):
    article = db.session.query(Articles).filter(Articles.id == id).first()
    creator = db.session.query(User).filter(User.id == article.creator).first()
    return render_template("news_template.html", article=article, creator=creator)


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
    return render_template("my_news.html", articles=article)


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
    return render_template('my_profile.html', title='мой профиль', form=form)


@bp.route('/get_poster', methods=['GET', 'POST'])
@login_required
def get_poster():
    form = GetPrivelegy()
    if form.validate_on_submit():
        if form.text.data == "Супер-пупер_секрeтный_код":
            current_user.position = 1
            db.session.commit()
            return redirect("/")
    return render_template('get_poster.html', title='Получить привелегию', form=form)
