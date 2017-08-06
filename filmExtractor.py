#-*- coding:utf-8 -*-

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required


app = Flask(__name__)
app.config['SECRET_KEY'] = 'misamisa is my wife'
bootstrap = Bootstrap(app)

class FilmForm(FlaskForm):
	hrefField = StringField(u'href', validators=[Required()])
	titleField = StringField(u'title', validators=[Required()])
	coverUrlField = StringField(u'cover_url', validators=[Required()])
	showTypeField = StringField(u'show_type')
	submit = SubmitField(u'提交')


@app.route('/', methods=['GET', 'POST'])
def index():
	form = FilmForm()
	return render_template('index.html', form=form)

if __name__ == '__main__':
	app.run(debug=True)