from flask import Blueprint, render_template, request, redirect, url_for, session

from app.model import Atricle

web_blue = Blueprint('web',__name__)
@web_blue.route('/index/',methods=['GET'])
def index():
    articles = Atricle.query.order_by(Atricle.id).all()
    return render_template('web/index.html',articles=articles)
@web_blue.route('/about/', methods=['GET'])
def about():
    return render_template('web/about.html')
@web_blue.route('/content/', methods=['GET'])
def content():
    articles = Atricle.query.order_by(Atricle.id).all()
    return render_template('web/content.html', articles=articles)
@web_blue.route('/sel_content/<int:id>', methods=['GET'])
def sel_content(id):
    articles = Atricle.query.order_by(Atricle.id).all()
    return render_template('web/content.html',articles=articles)

