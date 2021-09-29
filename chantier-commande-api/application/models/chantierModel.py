from application.models.commande import bceLineModel
from application.schemas.commande.bceSchema import BceSchema
from marshmallow.fields import DateTime
from application.models.commande.bceModel import BceModel
from flask import current_app
from application.om import OdooModel as om 
from application.models.enginModel import EnginModel
from application.models.employyeModel import EmployeeModel
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

            notifRes = BceModel.get_bce_by_ch_id(ch_id,user,data=['name','create_date'],notif=True) 
                
            bce_count = BceModel.get_count_bce_by_ch_id(ch_id,user)
            firstId = BceModel.get_first_bce_by_ch_id(ch_id,user)
            res.append({
                        "id":ch_id,
                        "name":chantier['chantier_id'][1],
                        "type":ch_info[0]['type'],
                        "engins":engins,
                        #"employees":employees,
                        "responsables":responsables,
                        "prices":numPrices,
                        "bce_count":bce_count,
                        "first_bce":firstId,
                        "commande":result,
                        "notification":notifRes
                        })
        """
        bce = BceModel("bce0023","ana",1179,"test note","ghi ana")
        to_fetch = {'name','demandeur','ch_id','service'}
        data = {'ch_id': 179, 'demandeur': 'ana', 'service': 'ghi ana', 'name': 'bce0023','type':'type'}
        odoo_data = {'create_uid': [98, 'POINTEUR'], 'employee_id': [2010, 'MAKHOUKHI HASSANE'],
 'create_date': '2021-03-09 10:08:44', 'name': 'BCE00032', 'service': 'Achat',
  'type_bon': 'Chantier', 'chantier_id': [179, 'AL HOCEIMA CONSTRUCTION DU BARRAGE SUR OUED RHISS'], 
  'state': 'draft', 'write_date': '2021-03-09 11:04:34', 'id': 32}
        bce = BceSchema().load(BceModel.transform_data(odoo_data,'client'))
        print(bce)
    """   
        return res