from application.db import db
from flask import current_app
import uuid
from cryptography.fernet import Fernet
from application.om import OdooModel as om
import base64


eKey = current_app.config['ENCRYPTION_KEY']


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer,  unique=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    public_id = db.Column(db.String(255))

    def __init__(self,uid,username,password,public_id):
        
        self.uid = uid
        self.username = username
        self.password = password
        self.public_id = public_id
    
    

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(public_id=_id).first()

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_public_id(cls, public_id: str) -> "UserModel":
        return cls.query.filter_by(public_id=public_id).first()
    
    def encryptMsg(Msg):
        return Fernet(str.encode(eKey)).encrypt(Msg.encode())
    
    def decryptMsg(self,Msg):
        return Fernet(str.encode(eKey)).decrypt(Msg.encode()).decode()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()