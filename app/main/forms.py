from flask_wtf import FlaskForm
from wtforms import StringField, FileField, TextAreaField, RadioField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    heading = StringField('Краткое описание статьи', validators=[DataRequired()])
    content = TextAreaField("Содержание", validators=[DataRequired()])
    category = RadioField("Выберите категорию",
                          choices=[
                                    ('1', "Games"),
                                    ('2', "Movies"),
                                    ('3', "Series"),
                                    ('4', "Books"),
                                    ],
                          default='1',
                          validators=[DataRequired()])
    file = FileField()


class MyProfile(FlaskForm):
    username = StringField('Никнейм', validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired()])
    position = StringField('Статус', validators=[DataRequired()])
    submit = SubmitField('Сохранить')


class GetPrivelegy(FlaskForm):
    text = StringField('Секретный код', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')


class CommentsCreateForm(FlaskForm):
    text = StringField('Введите коментарий', validators=[DataRequired()])
    submit = SubmitField('Отправить')
