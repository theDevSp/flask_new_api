from flask import current_app
from application.om import OdooModel as om 


oModel = om.ODOO_MODEL
oCommon = om.ODOO_COMMON
oDB = om.ODOO_DB

class ResponsableModel():

    _model_resp = 'fleet.vehicle.chantier.responsable'

    def __init__(self,id,name,job):
        self.id = id
        self.name = name
        self.job = job

    @classmethod
    def get_responsable_by_ch_id(cls,ch_id,user):
        
        res = []

        responsable_list = oModel.execute_kw(oDB, user.uid, user.decryptMsg(user.password),
                        cls._model_resp, 'search_read',[[['chantier_id', '=', ch_id],['current', '=',True]]],{'fields': ['employee_id','job_id']})
        
        for responsable in responsable_list:
            if not "pointeur" in responsable['job_id'][1].lower():
                res.append({
                    "id":responsable['employee_id'][0] if not isinstance(responsable['employee_id'][0],bool) else 0,
                    "name":responsable['employee_id'][1] if not isinstance(responsable['employee_id'][1],bool) else '',
                    "job":responsable['job_id'][1] if not isinstance(responsable['job_id'],bool) else ''
                })
            
        return res
    
    @classmethod
    def get_responsable_by_id(cls,resp_id,user):
        
        res = []

        responsable_list = oModel.execute_kw(oDB, user.uid, user.decryptMsg(user.password),
                        cls._model_resp, 'search_read',[[['employee_id', '=', resp_id]]],{'fields': ['employee_id','job_id']})
        
        for responsable in responsable_list:
            
            
            res.append({
                "id":responsable['employee_id'][0] if not isinstance(responsable['employee_id'][0],bool) else 0,
                "name":responsable['employee_id'][1] if not isinstance(responsable['employee_id'][1],bool) else '',
                "job":responsable['job_id'][1] if not isinstance(responsable['job_id'],bool) else ''
            })

        return res
