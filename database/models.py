from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer
from sqlalchemy.sql.sqltypes import Boolean
from config import SQLALCHEMY_DATABASE_URI

db = SQLAlchemy()

def setup_db(app, database_path=SQLALCHEMY_DATABASE_URI):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)   
    print(database_path)
    return db


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    subscribed = Column(Boolean, default=False, nullable=False)
    auth0_id = Column(String, default="", nullable=False)

    def insert(self):
        db.session.merge(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def format(self):
        return {
            'id': self.id,
            'email': self.email,
            'subscribed': self.subscribed,
            'auth0_id': self.auth0_id
        }