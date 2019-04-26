import redis
from flask import Flask
from flask_script import Manager
from flask_session import Session

from app.model import db
from app.views import back_blue
from web.views import web_blue
import pymysql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:rock1204@localhost:3306/blog1'
app.secret_key = 'fdafdfdasgafhfafdgfa'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1',port=6379)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.register_blueprint(blueprint=back_blue, url_prefix='/back')
app.register_blueprint(blueprint=web_blue, url_prefix='/web')
Session(app)
manage = Manager(app)
if __name__ == '__main__':
    manage.run()

