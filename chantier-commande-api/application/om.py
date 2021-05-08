from flask import current_app
import xmlrpc.client as xmlrpclib


class OdooModel:
    
    ODOO_URL = current_app.config['DB_URL']
    ODOO_DB = current_app.config['DB_NAME']
    ODOO_COMMON = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format("http://192.168.1.205:3389"))
    ODOO_MODEL = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format("http://192.168.1.205:3389"))