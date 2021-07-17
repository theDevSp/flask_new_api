from xmlrpc.client import SYSTEM_ERROR
from flask import current_app,jsonify
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Resource
from sqlalchemy.engine import create_engine
from application.om import OdooModel as om
import sys
import xlrd

#eKey = current_app.config['ENCRYPTION_KEY']
oModel = om.ODOO_MODEL
oCommon = om.ODOO_COMMON
oDB = om.ODOO_DB


class add(Resource):

    @classmethod
    def get(cls):
            data=[]
            """
            loc = ("application/ressources/data_to_insert.xlsx")
 
            wb = xlrd.open_workbook(loc)
            sheet = wb.sheet_by_index(0)
            i = 0
            while i < 511:
                data.append(
                    {
                        'type' : 'add',
                      'holiday_status_id' : 5,
                      'employee_id' : int(sheet.cell_value(i, 0)),
                      'name' : 'MAJ/01/07/2021',
                      'number_of_days_temp' : sheet.cell_value(i, 1),
                      'holiday_type':'employee',
                      
            }
                )
                created_bce_id = oModel.execute_kw(oDB,  1, '1990-', 'hr.holidays', 'create', [{
                        'type' : 'add',
                      'holiday_status_id' : 5,
                      'employee_id' : int(sheet.cell_value(i, 0)),
                      'name' : 'MAJ/01/07/2021',
                      'number_of_days_temp' : sheet.cell_value(i, 1),
                      'holiday_type':'employee',
                      
            }])
                
            
                oModel.execute_kw(oDB,  1, '1990-', 'hr.holidays', 'write', [created_bce_id,{'state':'validate'}])  
                print("created for " + sheet.cell_value(i, 2))  
            
                i+=1
            """    
            engine = create_engine('postgresql://simple_user:ftp5432postgres#@192.168.1.205:5432/newDB')
            result_set = engine.execute("select id,name from res_partner where id in (select distinct(partner_id) from purchase_order where chantier_id = 179 and bce_chantier in (select distinct(id) from stock_external_move where chantier_id = 179 and type_bon = 'Chantier')) order by id;")  
            for r in result_set:  
                print(r)
            return  jsonify(json_list = result_set.all())
            