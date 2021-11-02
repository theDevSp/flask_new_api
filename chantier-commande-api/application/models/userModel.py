from application.models.chantierModel import ChantierModel
from application import InvalidUsage
from application.db import db
from flask import current_app
import uuid
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from cryptography.fernet import Fernet
from application.om import OdooModel as om
import sys
from sqlalchemy.exc import SQLAlchemyError



eKey = current_app.config['ENCRYPTION_KEY']
oModel = om.ODOO_MODEL
oCommon = om.ODOO_COMMON
oDB = om.ODOO_DB



class UserModel(db.Model):
    
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer,  unique=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    public_id = db.Column(db.String(255))
    employee_id = db.Column(db.Integer,  unique=True)
    role = db.Column(db.Integer)

    def __init__(self,uid,username,password,public_id,employee_id,role):
        
        self.uid = uid
        self.username = username
        self.password = password
        self.public_id = public_id
        self.employee_id = employee_id
        self.role = role
    
    

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(public_id=_id).first()

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        try:
            return cls.query.filter_by(username=username).first()
        except Exception:
            raise InvalidUsage(str(sys.exc_info()[1]).split(':')[0] + ", Erreur base de Donnée" )
        
    
    @classmethod
    def find_by_public_id(cls, public_id: str) -> "UserModel":
        try:
            return cls.query.filter_by(public_id=public_id).first()
        except Exception:
            raise InvalidUsage(str(sys.exc_info()[1]).split(':')[0] + ", Erreur base de Donnée" )
        

    @classmethod
    @jwt_required(optional=True)
    def login(cls,username,password,userSchema):
        
        try:
            uid = oCommon.authenticate(oDB, username, password, {})
        except Exception:
            raise InvalidUsage(str(sys.exc_info()[1]))
        
        
        if uid:
            
            encrypted_pass = cls.encryptMsg(password)
            employee_id = oModel.execute_kw(oDB, uid, password,
                        'res.users', 'read', [uid], {'fields': ['employee_id','role']})
            new_user = {'uid':uid,'username':username,'password':encrypted_pass,'public_id':str(uuid.uuid4()),'employee_id':employee_id['employee_id'][0],'role':employee_id['role']}
            
            try:
                user_if_exist = cls.find_by_username(username)
            except Exception:
                raise InvalidUsage(str(sys.exc_info()[1]))
            
            user = userSchema.load(new_user)
            identity = None
            if user_if_exist:
                identity = user_if_exist.public_id = str(uuid.uuid4())
                try:
                    user_if_exist.save_to_db()
                except Exception:
                    raise InvalidUsage(str(sys.exc_info()[1]), status_code=500)
            else:
                identity = new_user.get('public_id',0)
                try:
                    user.save_to_db()
                except Exception:
                    raise InvalidUsage(str(sys.exc_info()[1]), status_code=500)
                
            return  identity
        else:
            raise InvalidUsage("Login ou mot de passe incorrect Veuillez réessayer")

        
    
    @classmethod
    def get_user_infos(cls,**kwargs):

        user = None

        models = [ 
                    'res.users',
                    'fleet.vehicle',
                    'fleet.vehicle.chantier',
                    'fleet.vehicle.chantier.users',
                    'fleet.vehicle.chantier.responsable'
                ]
            
        if kwargs:
            if 'public_id' in kwargs:
                user = cls.find_by_public_id(kwargs.get('public_id'))
            if 'username' in kwargs:
                user = cls.find_by_username(kwargs.get('username'))
                           
            if om.check_access_rights(user,'read',*models) == True:

                try:
                    res = oModel.execute_kw(oDB, user.uid, user.decryptMsg(user.password),
                        'res.users', 'read', [user.uid], {'fields': ['employee_id','role','login_date']})
                    
                except Exception:
                    raise InvalidUsage(str(sys.exc_info()[1]), status_code=410)
                    
                return {
                        "id":res['employee_id'][0] if not isinstance(res['employee_id'],bool) else 0,
                        "name":res['employee_id'][1] if not isinstance(res['employee_id'],bool) else '',
                        "role":res.get("role",0),
                        "uid":user.uid
                    }
            else:
                raise InvalidUsage(str(om.check_access_rights(user,'read',*models)), status_code=410) 

        return False
    
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
    


