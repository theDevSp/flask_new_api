from application.ressources.errors import InvalidUsage

from flask import current_app
from application.om import OdooModel as om 
from application.models.documentsLineModel import DocumentsLineModel
import sys


oModel = om.ODOO_MODEL
oCommon = om.ODOO_COMMON
oDB = om.ODOO_DB

class BceLineModel(DocumentsLineModel):

    _model_bce_line = 'article.commande'

    def __init__(self,ref, product, qty, vehicle_id, note,num_prix_id,bce_id, created_by, create_date, write_date, id):
        super().__init__(product, qty, vehicle_id, note, created_by=created_by, create_date=create_date, write_date=write_date, id=id)

        self.num_prix_id = num_prix_id
        self.bce_id = bce_id
        self.ref = ref
    
    @classmethod
    def create_bce_line(cls,data,user):

        bce_line_data = cls.transform_data(data)

        try:
            created_bce_line_id = oModel.execute_kw(oDB,  user.uid, user.decryptMsg(user.password), cls._model_bce_line, 'create', [bce_line_data])
        except Exception:
            raise InvalidUsage(str(sys.exc_info()[1]))
        
        return cls.get_bce_line_by_id(created_bce_line_id,user,['name','create_uid','create_date','write_date',"ref_external"])

    @classmethod
    def update_bce_line(cls,id,data,user):

        bce_line_data = cls.transform_data(data)
        cols = list(bce_line_data.keys()) + ["write_date"]
        
        try:
            oModel.execute_kw(oDB,  user.uid, user.decryptMsg(user.password), cls._model_bce_line, 'write', [id,bce_line_data])
            updated = cls.get_bce_line_by_id(id,user,cols)
        except Exception:
            raise InvalidUsage(str(sys.exc_info()[1]))
        
        return updated

    @classmethod
    def delete_bce_line(cls,id,user):

        try:
            deleted = oModel.execute_kw(oDB,  user.uid, user.decryptMsg(user.password), cls._model_bce_line, 'unlink', [[id]])

        except Exception:
            raise InvalidUsage(str(sys.exc_info()[1]))
        
        return deleted

    @classmethod
    def get_bce_line_by_id(cls,id,user,data=['name','qty_external','vehicle_id','num_prix_id','create_date','external_id','create_uid','ref_external','note','write_date']):

        try:
            res = oModel.execute_kw(oDB,  user.uid, user.decryptMsg(user.password), cls._model_bce_line, 'search_read',[[['id', '=', id]]],{'fields': data})
        except Exception:
            raise InvalidUsage(str(sys.exc_info()[1]))

        return cls.transform_data(res,'client')[0]
    
    @classmethod
    def get_bce_line_by_bce_id(cls,bce_id,user,data=['name','qty_external','vehicle_id','num_prix_id','create_date','external_id','create_uid','ref_external','note','write_date']):

        try:
            res = oModel.execute_kw(oDB,  user.uid, user.decryptMsg(user.password), cls._model_bce_line, 'search_read',[[['external_id', '=', bce_id]]],{'fields': data})
        except Exception:
            raise InvalidUsage(str(sys.exc_info()[1]))

        return cls.transform_data(res,'client')
    
    @classmethod
    def get_count_bce_line_by_bce_id(cls,bce_id,user):

        try:
            res = oModel.execute_kw(oDB,  user.uid, user.decryptMsg(user.password), cls._model_bce_line, 'search_count',[[['external_id', '=', bce_id]]])
        except Exception:
            raise InvalidUsage(str(sys.exc_info()[1]))

        return res

    @classmethod
    def transform_data(cls,datas,direction='odoo'):

        if direction == 'odoo':
            
            if 'product' in datas:
                datas[datas.index('product')] = 'name'
            if 'qty' in datas:
                datas[datas.index('qty')] = 'qty_external'
            if 'ref' in datas:
                datas[datas.index('ref')] = 'ref_external'
            if 'bce_id' in datas:
                datas[datas.index('bce_id')] = 'external_id'
                

            
        else:

            for data in datas:
                if 'create_uid' in data:
                    data['create_uid'] = data['create_uid'][1]
                    data['created_by'] = data.pop('create_uid')
                if 'vehicle_id' in data:
                    data['vehicle_id'] = data['vehicle_id'][0] if data['vehicle_id'] else 0
                if 'num_prix_id' in data:
                    data['num_prix_id'] = data['num_prix_id'][0] if data['num_prix_id'] else 0
                if 'external_id' in data:
                    data['external_id'] = int(data['external_id'][0])
                    data['bce_id'] = data.pop('external_id')
                if 'name' in data:
                    data['product'] = data.pop('name')
                if 'ref_external' in data:
                    data['ref'] = data.pop('ref_external')
                if 'qty_external' in data:
                    data['qty'] = data.pop('qty_external')

        return datas


"""
'article.commande', 'search_read',
    [[['external_id', '=', external_id]]],
    {'fields': [
        'name','qty_external','vehicle_id',
        'num_prix_id','create_date','external_id','create_uid','ref_external','note','write_date'
    ]})

"""