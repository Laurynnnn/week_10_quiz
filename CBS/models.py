from os import link
from turtle import title
from CBS import db
from datetime import datetime
import sqlite3


class ExtraMixin(object):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()


#CBS News model
class CBSNews(db.Model, ExtraMixin):
    __tablename__ =  'cbs_news'
    title = db.column(db.String(100), nullable = False)
    link = db.column(db.String(100), nullable = False)
    image = db.column(db.String(100), nullable = False)
    description = db.column(db.String(500), nullable = False)
    
    @classmethod
    def get_cbs_news(cls):
        return cls.query.all()
        
