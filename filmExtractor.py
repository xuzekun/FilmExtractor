#-*- coding:utf-8 -*-

from flask import Flask, render_template, request,  jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required
from wtforms.widgets import TextArea
import json
from videoSpider import VideoSpider
import logging
import os
import time

def initLogger():
	logdir = 'logs'
	if not os.path.exists(logdir):
		os.mkdir(logdir)

	logging.basicConfig(level=logging.DEBUG,
		format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        #datefmt='%a, %d %b %Y %H:%M:%S',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename= logdir + '/FilmExtractor.log.'+time.strftime('%Y_%m_%d_%H'),
        filemode='a'
		)

	# 将DEBUG级别以上的日志输出屏幕
	console = logging.StreamHandler()
	console.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d %(levelname)s %(message)s]')
	console.setFormatter(formatter)
	logging.getLogger('logs').addHandler(console)

# initlogger
initLogger()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'misamisa is my wife'
bootstrap = Bootstrap(app)


class PicForm(FlaskForm):
	urlField = StringField(u'URL(*)', validators=[Required()])
	hrefField = StringField(u'href xpath(*)', validators=[Required()])
	titleField = StringField(u'title xpath(*)', validators=[Required()])
	coverUrlField = StringField(u'cover_url xpath(*)', validators=[Required()])
	showTypeField = StringField(u'show_type')
	prefixUrlField = StringField(u'prefixUrl')
	encodingField = StringField(u'encoding')
	submit = SubmitField(u'提交')

class NoPicForm(FlaskForm):
	urlField = StringField(u'URL(*)', validators=[Required()])
	hrefField = StringField(u'href xpath(*)', validators=[Required()])
	titleField = StringField(u'title xpath(*)', validators=[Required()])
	coverUrlField = StringField(u'cover_url xpath(*)', validators=[Required()])
	showTypeField = StringField(u'show_type')
	prefixUrlField = StringField(u'prefixUrl')
	encodingField = StringField(u'encoding')
	submit = SubmitField(u'提交')


@app.route('/', methods=['GET', 'POST'])
def index():
	form = PicForm()
	outputData = dict()

	if request.method == 'GET':
		logging.info("get /index")

	if request.method == 'POST' and form.validate_on_submit():
		logging.info(request.form)
		#construct requestData
		requestData = dict()
		requestData['url'] = request.form['urlField']
		requestData['encoding'] = request.form['encodingField']
		getInfo = dict()
		getInfo['href'] = request.form['hrefField']
		getInfo['title'] = request.form['titleField']
		getInfo['coverUrl'] = request.form['coverUrlField']
		getInfo['showType'] = request.form['showTypeField']
		getInfo['prefix_url'] = request.form['prefixUrlField']
		requestData['getInfo'] = getInfo

		jsontData = json.dumps(requestData, ensure_ascii=False)

		# spdering
		spider = VideoSpider()
		outputData =  spider.getPicInfo(jsontData)
		logging.debug(outputData)
		
	return render_template('index.html', form=form,output=outputData)

@app.route('/noPic', methods=['GET', 'POST'])
def noPic():
	form = NoPicForm()
	outputData = dict()

	if request.method == 'GET':
		logging.info("get /nopic")

	if request.method == 'POST' and form.validate_on_submit():
		logging.info(request.form)
		# construct requestData
		requestData = dict()
		requestData['url'] = request.form['urlField']
		requestData['encoding'] = request.form['encodingField']
		getLink = dict()
		getLink['href'] = request.form['hrefField']
		getLink['title'] = request.form['titleField']
		getLink['coverUrl'] = request.form['coverUrlField']
		getLink['showType'] = request.form['showTypeField']
		getLink['prefix_url'] = request.form['prefixUrlField']
		requestData['getLink'] = getLink

		jsontData = json.dumps(requestData, ensure_ascii=False)

		# spidering
		spider = VideoSpider()
		outputData =  spider.getNoPicInfo(jsontData)
		logging.debug(outputData)

	return render_template('noPic.html', form=form, output=outputData)





if __name__ == '__main__':
	initLogger()
	app.run(debug=True,host='0.0.0.0',port=46464)