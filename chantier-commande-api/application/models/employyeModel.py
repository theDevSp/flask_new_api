from flask import current_app
from application.om import OdooModel as om 
from application.models.enginModel import EnginModel

#eKey = current_app.config['ENCRYPTION_KEY']
oModel = om.ODOO_MODEL
oCommon = om.ODOO_COMMON
oDB = om.ODOO_DB

class EmployeeModel():

    _model_emp = 'hr.employee'
    _model_contract = 'hr.contract'

    def __init__(self,id,name,cin,job,vehicle,emp_type):
        self.id = id
        self.name = name
        self.cin = cin
        self.job = job
        self.vehicle = vehicle
        self.emp_type = emp_type
    
    @classmethod
    def get_employee_by_ch_id(cls,ch_id,user):
        
        res = []

        employee_list = oModel.execute_kw(oDB, user.uid, user.decryptMsg(user.password),
                        cls._model_emp, 'search_read',[[['chantier_id', '=', ch_id]]],{'fields': ['name','job_id','vehicle_id','identification_id','base_hours']})
        
        for employee in employee_list:
            
            
            res.append({
                "id":employee.get("id",0),
                "cin":employee['identification_id'] if not isinstance(employee['identification_id'],bool) else '',
                "name":employee['name'] if not isinstance(employee['name'],bool) else '',
                "job":employee['job_id'][1] if not isinstance(employee['job_id'],bool) else '',
                "vehicle":employee['vehicle_id'][1] if not isinstance(employee['vehicle_id'],bool) else '',
                "base_hours":employee['base_hours']
            })
        return res
    
    @classmethod
    def get_employee_by_id(cls,id,user):
        
        res = []

        employee_list = oModel.execute_kw(oDB, user.uid, user.decryptMsg(user.password),
                        cls._model_emp, 'search_read',[[['id', '=', id]]],{'fields': ['name','job_id','vehicle_id','identification_id','base_hours']})
        
        for employee in employee_list:
            
            
            res.append({
                "id":employee.get("id",0),
                "cin":employee['identification_id'] if not isinstance(employee['identification_id'],bool) else '',
                "name":employee['name'] if not isinstance(employee['name'],bool) else '',
                "job":employee['job_id'][1] if not isinstance(employee['job_id'],bool) else '',
                "vehicle":employee['vehicle_id'][1] if not isinstance(employee['vehicle_id'],bool) else '',
                "base_hours":employee['base_hours']
            })
        return res

    @classmethod
    def get_employee_hours_days(cls,contract_id,user):

        data = oModel.execute_kw(oDB, user.uid, user.decryptMsg(user.password),
                        cls._model_contract, 'search_read',[[['id', '=', contract_id]]],{'fields': ['working_hours_per_day','working_days_per_week']})
        
        return data
