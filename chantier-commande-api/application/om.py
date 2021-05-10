from flask import current_app
import xmlrpc.client as xmlrpclib


class OdooModel:
    
    ODOO_URL = current_app.config['DB_URL']
    ODOO_DB = current_app.config['DB_NAME']
    ODOO_COMMON = ''
    ODOO_MODEL = ''
    if ODOO_URL:
        ODOO_COMMON = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(str(ODOO_URL)))
        ODOO_MODEL = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(str(ODOO_URL)))

    @classmethod
    def check_access_rights(cls,user,module,option):
        if not cls.ODOO_MODEL.execute_kw(cls.ODOO_DB, user.uid, user.decryptMsg(user.password),module, 'check_access_rights',[option], {'raise_exception': False}):
            return False
        return True 