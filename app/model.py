from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(10),unique=True,nullable=False)
    password =db.Column(db.String(255),nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    __tablename__ = 'user'
    def save_update(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
class ArticleType(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    a_name = db.Column(db.String(10),nullable=False,unique=False)
    t_name = db.Column(db.String(10), nullable=False, unique=True)
    artsfr = db.relationship('Atricle', backref='tp')
    __tablename__ = 'art_type'


class Atricle(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), unique=True,nullable=False)
    describ = db.Column(db.String(100), nullable=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    type = db.Column(db.Integer, db.ForeignKey('art_type.id'))
