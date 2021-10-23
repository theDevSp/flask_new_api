from application.models.commande import bceLineModel
from application.schemas.commande.bceSchema import BceSchema
from marshmallow.fields import DateTime
from application.models.commande.bceModel import BceModel
from flask import current_app
from application.om import OdooModel as om 
from application.models.enginModel import EnginModel
from application.models.entries.entriesModel import EntriesModel
from application.models.responsable import ResponsableModel
from application.models.numPrixModel import NumPrixModel
import datetime as dt
oModel = om.ODOO_MODEL
oCommon = om.ODOO_COMMON
oDB = om.ODOO_DB

class ChantierModel():

    _model_ch = 'fleet.vehicle.chantier'
    _model_ch_users = [
        'fleet.vehicle.chantier.users',
        'fleet.vehicle.chantier.pointeur',
        'fleet.vehicle.chantier.chef',
        ]

    def __init__(self,id,name,use,atelier):
        self.id = id
        self.name = name
        self.use = use
        self.atelier = atelier


    @classmethod
    def get_chantier_by_user_id(cls,user):
        
        res = []
        chantierList = []
        model = ''
        if user.role in [4,5,6,7]:
            model = cls._model_ch_users[1]
        elif user.role == 3:
            model = cls._model_ch_users[0]
        else:
            model = cls._model_ch_users[2]
        chantierList = oModel.execute_kw(oDB, user.uid, user.decryptMsg(user.password),
                 model, 'search_read',
                [[['employee_id','=',user.employee_id]]],{'fields': ['chantier_id']})
        
        for chantier in chantierList:
            ch_id = chantier['chantier_id'][0]
            ch_info = oModel.execute_kw(oDB, user.uid, user.decryptMsg(user.password),
                    cls._model_ch, 'search_read',[[['id','=',ch_id]]],{'fields': ['usinage','atelier_stock','type']})
            engins = EnginModel.get_engin_by_ch_id(ch_id,user)
            #employees = EmployeeModel.get_employee_by_ch_id(ch_id,user)
            responsables = ResponsableModel.get_responsable_by_ch_id(ch_id,user)
            if not ch_info[0]['type']:
                numPrices = NumPrixModel.get_price_numbers_by_ch_id(ch_id,user)

            result = BceModel.get_bce_by_ch_id(ch_id,user)    
            for ftched in result:
                #ftched['line'] = bceLineModel.BceLineModel.get_bce_line_by_bce_id(ftched['id'],user,)
                ftched['line_count'] = bceLineModel.BceLineModel.get_count_bce_line_by_bce_id(ftched['id'],user)

            notifRes = BceModel.get_bce_by_ch_id(ch_id,user,data=['name','create_date','state'],notif=True) 
                
            bce_count = BceModel.get_count_bce_by_ch_id(ch_id,user)
            bce_count_chantier = BceModel.get_count_bce_by_ch_id_type(ch_id,user,'Chantier')
            bce_count_engin = BceModel.get_count_bce_by_ch_id_type(ch_id,user,'Engin')
            bce_count_achat = BceModel.get_count_bce_by_ch_id_service(ch_id,user,'Achat')
            bce_count_magasin = BceModel.get_count_bce_by_ch_id_service(ch_id,user,'Magasin')
            firstId = BceModel.get_first_bce_by_ch_id(ch_id,user)
            bce_count_date = BceModel.get_count_bce_by_ch_id_periode(ch_id,user)
            entries = EntriesModel.get_entries_by_ch_period(ch_id,str(dt.datetime.now().year),str(dt.datetime.now().month-1))
            
            res.append({
                        "id":ch_id,
                        "name":chantier['chantier_id'][1],
                        "type":ch_info[0]['type'],
                        "engins":engins,
                        #"employees":employees,
                        "responsables":responsables,
                        "prices":numPrices,
                        "bce_count":bce_count,
                        "bce_count_chantier":bce_count_chantier,
                        "bce_count_engin":bce_count_engin,
                        "bce_count_achat":bce_count_achat,
                        "bce_count_magasin":bce_count_magasin,
                        "bce_count_date":bce_count_date,
                        "first_bce":firstId,
                        "commande":result,
                        "notification":notifRes,
                        "entries":entries
                        })
  
        return res