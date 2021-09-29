from xmlrpc.client import SYSTEM_ERROR
from flask import current_app,jsonify
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Resource
import sqlalchemy
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
            
            loc = ("application/ressources/stc.xlsx")
 
            wb = xlrd.open_workbook(loc)
            sheet = wb.sheet_by_index(0)
            i = 0
            while i < 16:
                engine = create_engine('postgresql://dbuser:cofabri1900@192.168.1.45:5432/newDB')
                result_set = engine.execute(sqlalchemy.text("select id from hr_employee where identification_id = :val"), val = sheet.cell_value(i, 1))  
                
                for r in result_set:  
                    
                    created_bce_id = oModel.execute_kw(oDB,  1, 'utnubu', 'hr.holidays', 'create', [{
                            'type' : 'add',
                        'holiday_status_id' : 5,
                        'employee_id' : r.id,
                        'name' : 'MAJ/01/07/2021',
                        'number_of_days_temp' : sheet.cell_value(i, 2),
                        'holiday_type':'employee',
                        
                }])
                    
                
                    oModel.execute_kw(oDB,  1, 'utnubu', 'hr.holidays', 'write', [created_bce_id,{'state':'validate'}])  
                    print("created for " + sheet.cell_value(i, 0))  
                
                i+=1
            """    
            engine = create_engine('postgresql://simple_user:ftp5432postgres#@192.168.1.205:5432/newDB')
            result_set = engine.execute("select id,name from res_partner where id in (select distinct(partner_id) from purchase_order where chantier_id = 179 and bce_chantier in (select distinct(id) from stock_external_move where chantier_id = 179 and type_bon = 'Chantier')) order by id;")  
            for r in result_set:  
                print(r)
            return  jsonify(json_list = result_set.all())
            """

class update(Resource):

        @classmethod
        def get(cls):
            loc = ("application/ressources/stc.xlsx")
 
            wb = xlrd.open_workbook(loc)
            sheet = wb.sheet_by_index(0)
            i = 0
            res =[]
            while i < 16:
                engine = create_engine('postgresql://dbuser:cofabri1900@192.168.1.45:5432/newDB')
                result_set = engine.execute(sqlalchemy.text("select id from hr_employee where identification_id = :val"), val = sheet.cell_value(i, 1))  
                
                for r in result_set:  
                    holidays_set = engine.execute(sqlalchemy.text("select * from hr_holidays where employee_id = :val"), val = r.id)
                    if holidays_set.rowcount> 0:
                        for h in holidays_set :
                            res.append(h.id)
                            
                            
                            #oModel.execute_kw(oDB,  1, 'utnubu', 'hr.holidays', 'unlink', [[h.id]])
                            #print("deleted " + h.name) 
                               
            
                i+=1
            for id in res:
                engine.execute(sqlalchemy.text("update hr_holidays set state='draft' where id = :val"), val = id)
                print(id)