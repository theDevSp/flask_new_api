import datetime
from application.ressources.errors import InvalidUsage


from application.om import OdooModel as om 
from application.models.documentsModel import DocumentsModel
from application.models.entries.entriesModel import EntriesModel
import sys


oModel = om.ODOO_MODEL
oCommon = om.ODOO_COMMON
oDB = om.ODOO_DB


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
        
        return cls.get_bce_by_id(created_bce_id,user)
    
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
        
        result = [{'commande':[]}]

        try:
            res = oModel.execute_kw(oDB,  user.uid, user.decryptMsg(user.password), cls._model_bce, 'search_read',[[['id', '=', id]]],
                        {'fields': data})
        except Exception:
            
            raise InvalidUsage(str(sys.exc_info()[1]))
        if res :
             result[0]['commande'] = cls.transform_data(res,'client')[0]

        return result
    
    @classmethod
    def get_bce_by_ch_id(cls,ch_id,user,data=['name','type_bon','employee_id','create_uid','service','create_date','state','chantier_id','write_date','note'],start=0,notif=False,startNotif=0):
        
        
        where = [['chantier_id', '=', ch_id]]
        limit=10
        if user.role in [3]:
            where.append(['type_bon','=','Engin'])
        if user.role in [2]:
            where.append(['type_bon','=','Chantier'])
        if start != 0:
            where.append(['id','<',start])
        if notif:
            where.append(['state','=','draft'])  
            where.append(['id','>',startNotif])
            limit=''
        
            
        try:
            res = oModel.execute_kw(oDB,  user.uid, user.decryptMsg(user.password), cls._model_bce, 'search_read',[where],{'fields': data,'limit':limit,'order':"id desc"})
           
        except Exception:
            
            raise InvalidUsage(str(sys.exc_info()[1]))

        return cls.transform_data(res,'client')
    
    @classmethod
    def get_filter_bce_by_ch_id(cls,ch_id,user,ref="",types="",services="",states="",date_start="",date_end="",start=0,data=['name','type_bon','employee_id','create_uid','service','create_date','state','chantier_id','write_date','note']):
        
        
        where = [['chantier_id', '=', ch_id]]
        if ref != "":
            where.append(['name','ilike',ref])
        else:
            
            
            if types != "":
                if types.endswith(','):
                    types = types[:-1]
                condition = []
                for type in types.split(','):
                    condition.append(type)
                where.append(['type_bon','in',[type]])
            else:
                if user.role in [3]:
                    where.append(['type_bon','=','Engin'])
                if user.role in [2]:
                    where.append(['type_bon','=','Chantier'])
            if services != "":
                if services.endswith(','):
                    services = services[:-1]
                condition = []
                for service in services.split(','):
                    condition.append(service)
                where.append(['service','in',[service]])
            if states != "":
                if states.endswith(','):
                    states = states[:-1]
                condition = []
                for state in states.split(','):
                    condition.append(state)
                where.append(['state','in',[state]])
            if len(date_start) > 0:
                
                where.append(['create_date','>=',date_start])
            if len(date_end) > 0:
                where.append(['create_date','<=',date_end])
            if start != 0:
                where.append(['id','<',start])
        
        
        
            
        try:
            res = oModel.execute_kw(oDB,  user.uid, user.decryptMsg(user.password), cls._model_bce, 'search_read',[where],{'fields': data,'limit':10,'order':"id desc"})
            
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
    def get_count_bce_by_ch_id_type(cls,ch_id,user,type):

        try:
            res = oModel.execute_kw(oDB,  user.uid, user.decryptMsg(user.password), cls._model_bce, 'search_count',[[['chantier_id','=',ch_id],['type_bon','=',type]]])
        except Exception:
            raise InvalidUsage(str(sys.exc_info()[1]))

        return res
    
    @classmethod
    def get_count_bce_by_ch_id_service(cls,ch_id,user,service):

        try:
            res = oModel.execute_kw(oDB,  user.uid, user.decryptMsg(user.password), cls._model_bce, 'search_count',[[['chantier_id','=',ch_id],['service','=',service]]])

        except Exception:
            raise InvalidUsage(str(sys.exc_info()[1]))

        return res

    @classmethod
    def get_count_bce_by_ch_id_periode(cls,ch_id,user):

        try:
            res = oModel.execute_kw(oDB,  user.uid, user.decryptMsg(user.password), cls._model_bce, 'read_group',[[('chantier_id','=',ch_id)],['create_date'],['create_date']])
            result = []
            temp_dict = {}
            for item in res:
                
                year = item['create_date'].split()[1]
                month_number = datetime.datetime.strptime(item['create_date'].split()[0], "%B").month 
                count = item['create_date_count']   
                if str(year) in temp_dict:
                    temp_dict[str(year)].append({
                        'm':month_number,
                        'c':count
                    })
                else:
                    temp_dict[str(year)] = []
                    temp_dict[str(year)].append({
                        'm':month_number,
                        'c':count
                    })
            for element in temp_dict.items():
                result.append(element)
            
        except Exception:
            raise InvalidUsage(str(sys.exc_info()[1]))

        return result

    @classmethod
    def get_first_bce_by_ch_id(cls,ch_id,user):

        where = [['chantier_id', '=', ch_id]]
        
        if user.role in [3,6]:
            where.append(['type_bon','=','Engin'])
        if user.role in [2,5]:
            where.append(['type_bon','=','Chantier'])

        try:
            res = oModel.execute_kw(oDB,  user.uid, user.decryptMsg(user.password), cls._model_bce, 'search_read',[where],{'fields': ['id'],'limit':1})
        except Exception:
            raise InvalidUsage(str(sys.exc_info()[1]))

        return res[0]['id']    

    @classmethod
    def transform_data(cls,datas,direction='odoo'):

        if direction == 'odoo':
            
            if 'demId' in datas:
                datas['employee_id'] = datas.pop('demId')
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
                    data['demId'] = data['employee_id'][0]
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
    def verify_action_permission(cls,id,data,user):
        state = cls.get_bce_by_id(id,user,['state'])[0]['commande']['state']
        
        if "state" in data:
            if "valid" in data["state"] and state != "draft":
                raise InvalidUsage("Action Non autorisée vous ne pouvez pas valider cette commande.")
            
            if "cancel" in data["state"] and cls.verify_bce_docs(id,user) > 0:
                raise InvalidUsage("Action Non autorisée cette commande est déjâ traitée vous ne pouvez pas l'annuler.")
            
            if "draft" in data["state"] and cls.verify_bce_docs(id,user) > 0 and state not in ['draft','valid','correct']:
                raise InvalidUsage("Action Non autorisée cette commande est déjâ traitée vous ne pouvez pas la modifier")
            
        return True
    
    @classmethod
    def verify_bce_docs(cls,id,user):
        res = 0

        try:
            res += oModel.execute_kw(oDB,  user.uid, user.decryptMsg(user.password), "stock.picking", 'search_count',[[['bce_chantier','=',id]]])
            res += oModel.execute_kw(oDB,  user.uid, user.decryptMsg(user.password), "purchase.requisition", 'search_count',[[['bce_chantier','=',id]]])
        except Exception:
            raise InvalidUsage(str(sys.exc_info()[1]))
        return res


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