from application.ressources.errors import InvalidUsage

from flask import current_app
from application.om import OdooModel as om 
from application.models.documentsModel import DocumentsModel
import sys


oModel = om.ODOO_MODEL
oCommon = om.ODOO_COMMON
oDB = om.ODOO_DB
engin = om.ENGIN

class BceModel(DocumentsModel):

    _model_bce = 'stock.external.move'
    _table = 'stock_external_move'

    def __init__(self, name, demandeur, ch_id,type,service,note=None,created_by=None,create_date=None,write_date=None,id=None,state=''):
        
        
        super().__init__(name, demandeur, ch_id, note=note, created_by=created_by, create_date=create_date, write_date=write_date, id=id, state=state)
        
        self.type = type
        self.service = service
        
    def __str__(self) -> str:
        return f"{self.name}"

    @classmethod
    def create_bce(cls,data,user):

        bce_data = cls.transform_data(data)

        try:
            created_bce_id = oModel.execute_kw(oDB,  user.uid, user.decryptMsg(user.password), cls._model_bce, 'create', [bce_data])
        except Exception:
            raise InvalidUsage(str(sys.exc_info()[1]))
        
        return cls.get_bce_by_id(created_bce_id,user,['name','create_uid','create_date','write_date'])
    
    @classmethod
    def update_bce(cls,id,data,user):

        bce_data = cls.transform_data(data)
        cols = list(bce_data.keys()) + ["write_date"]

        try:
            oModel.execute_kw(oDB,  user.uid, user.decryptMsg(user.password), cls._model_bce, 'write', [id,bce_data])
            updated = cls.get_bce_by_id(id,user,cols)
        except Exception:
            raise InvalidUsage(str(sys.exc_info()[1]))
        
        return updated
    
    @classmethod
    def delete_bce(cls,id,user):

        try:
            deleted = oModel.execute_kw(oDB,  user.uid, user.decryptMsg(user.password), cls._model_bce, 'unlink', [[id]])

        except Exception:
            raise InvalidUsage(str(sys.exc_info()[1]))
        
        return deleted
        
    @classmethod
    def get_bce_by_id(cls,id,user,data=['name','type_bon','employee_id','create_uid','service','create_date','state','chantier_id','write_date','note']):
        
        result = {'commande':[]}

        try:
            res = oModel.execute_kw(oDB,  user.uid, user.decryptMsg(user.password), cls._model_bce, 'search_read',[[['id', '=', id]]],
                        {'fields': data})
        except Exception:
            raise InvalidUsage(str(sys.exc_info()[1]))
        if res :
             result['commande'] = cls.transform_data(res,'client')[0]

        return result
    
    @classmethod
    def get_bce_by_ch_id(cls,ch_id,user,data=['name','type_bon','employee_id','create_uid','service','create_date','state','chantier_id','write_date','note'],start=0,notif=False):
        """
        cols = cls.getColumnsFromList(data)
        query = "select %s from %s where chantier_id = %s order by id DESC;" % (cols,cls._table,ch_id)result_set = engin.execute(query)  
        for r in result_set:  
            print(r.create_date)
        """
        where = [['chantier_id', '=', ch_id]]
        limit=10
        if user.role in [3,6]:
            where.append(['type_bon','=','Engin'])
        if user.role in [2,5]:
            where.append(['type_bon','=','Chantier'])
        if start != 0:
            where.append(['id','<',start])
        if not notif:
            where.append(['state','!=','draft'])  
        else: 
            where.append(['state','=','draft'])
            limit=''
        

        try:
            res = oModel.execute_kw(oDB,  user.uid, user.decryptMsg(user.password), cls._model_bce, 'search_read',[where],{'fields': data,'limit':limit,'order':"id desc"})
        except Exception:
            raise InvalidUsage(str(sys.exc_info()[1]))

        return cls.transform_data(res,'client')
    
    @classmethod
    def get_count_bce_by_ch_id(cls,ch_id,user):

        try:
            res = oModel.execute_kw(oDB,  user.uid, user.decryptMsg(user.password), cls._model_bce, 'search_count',[[['chantier_id','=',ch_id]]])
        except Exception:
            raise InvalidUsage(str(sys.exc_info()[1]))

        return res
        

    @classmethod
    def transform_data(cls,datas,direction='odoo'):

        if direction == 'odoo':
            
            if 'demandeur' in datas:
                datas['employee_id'] = datas.pop('demandeur')
            if 'type' in datas:
                datas['type_bon'] = datas.pop('type')
            if 'ch_id' in datas:
                datas['chantier_id'] = datas.pop('ch_id')
            
        else:

            for data in datas:
                if 'create_uid' in data:
                    data['create_uid'] = data['create_uid'][1]
                    data['created_by'] = data.pop('create_uid')
                if 'employee_id' in data:
                    data['employee_id'] = data['employee_id'][1]
                    data['demandeur'] = data.pop('employee_id')
                if 'chantier_id' in data:
                    data['chantier_id'] = int(data['chantier_id'][0])
                    data['ch_id'] = data.pop('chantier_id')
                if 'type_bon' in data:
                    data['type'] = data.pop('type_bon')
                if 'note' in data:
                    if isinstance(data['note'],bool): data['note'] = '' 
        
        return datas
    @classmethod
    def getColumnsFromList(cls,s): 
        str1 = "" 
        str1 = ','.join(map(str, s))  
        return str1
"""
{'create_uid': [98, 'POINTEUR'], 'employee_id': [2010, 'MAKHOUKHI HASSANE'],
 'create_date': '2021-03-09 10:08:44', 'name': 'BCE00032', 'service': 'Achat',
  'type_bon': 'Chantier', 'chantier_id': [179, 'AL HOCEIMA CONSTRUCTION DU BARRAGE SUR OUED RHISS'], 
  'state': 'draft', 'write_date': '2021-03-09 11:04:34', 'id': 32}
"""