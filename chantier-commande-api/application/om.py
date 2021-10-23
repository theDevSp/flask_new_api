from flask import current_app
import xmlrpc.client as xmlrpclib
import sys

from sqlalchemy.engine import create_engine
from application.ressources.errors import InvalidUsage



class OdooModel:
    
    ODOO_URL = current_app.config['ODOO_URL']
    ODOO_DB = current_app.config['DB_NAME']
    ODOO_COMMON = ''
    ODOO_MODEL = ''
    ENGIN = ''
    
    DB_URL = current_app.config['DB_URL']
    DB_CREDENTIAL = current_app.config['DB_CREDENTIAL']

    ENGIN = create_engine(str(DB_CREDENTIAL))


    if ODOO_URL:
        ODOO_COMMON = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(str(ODOO_URL)))
        ODOO_MODEL = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(str(ODOO_URL)))

    @classmethod
    def check_access_rights(cls,user,option,*args):
        
        if user:    
            for module in args:
                try:
                    res = cls.ODOO_MODEL.execute_kw(cls.ODOO_DB, user.uid, user.decryptMsg(user.password),module, 'check_access_rights',[option], {'raise_exception': False})
                except Exception:
                    raise InvalidUsage(str(sys.exc_info()[1]))
                    
                if not res :
                    raise InvalidUsage("User {} has no {} right to access {}".format(user.username,option,module), status_code=403)
        else:
            raise InvalidUsage("Aucun utilisateur trouver ou session expirée.")       
        return True 



