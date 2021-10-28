from flask import current_app
from application.om import OdooModel as om

#eKey = current_app.config['ENCRYPTION_KEY']
oModel = om.ODOO_MODEL
oCommon = om.ODOO_COMMON
oDB = om.ODOO_DB

class EnginModel():

    _model_gmao = 'fleet.vehicle'

    def __init__(self,id,name,plate,code,desc,brand):
        self.id = id
        self.name = name
        self.plate = plate
        self.code = code
        self.desc  = desc
        self.brand = brand

    @classmethod
    def get_engin_by_ch_id(cls,ch_id,user):
        res = []

        enginList = oModel.execute_kw(oDB, user.uid, user.decryptMsg(user.password),
                cls._model_gmao, 'search_read',
                [[['chantier_id', '=', ch_id],['state_breakdown','not in',('vendu','rendu','deteriore')]]],
                {'fields': ['code','license_plate','product_id','designation_id','brand_id','emplacement_chantier_id','state_breakdown','capacity']})
        for engin in enginList:
            res.append({
                "id":engin.get("id",0),
                "name":engin['product_id'][1] if not isinstance(engin['product_id'],bool) else '',
                "plate":engin['license_plate'] if not isinstance(engin['license_plate'],bool) else '',
                "code":engin.get('code',''),
                "desc":engin['designation_id'][1] if not isinstance(engin['designation_id'],bool) else '',
                "brand":engin['brand_id'][1] if not isinstance(engin['brand_id'],bool) else '',
                "place":engin['emplacement_chantier_id'][1].capitalize() if not isinstance(engin['emplacement_chantier_id'],bool) else 'Indéfini',
                "state":engin.get('state_breakdown','').capitalize() if not isinstance(engin.get('state_breakdown',''),bool) else 'Indéfini',
                "capacity":engin.get('capacity','') if not isinstance(engin.get('capacity',''),bool) else 'Indéfini',
            })
        return res

    @classmethod
    def get_engin_by_id(cls,id,user):
        res = []

        enginList = oModel.execute_kw(oDB, user.uid, user.decryptMsg(user.password),
                cls._model_gmao, 'search_read',
                [[['id', '=', id]]],{'fields': ['code','license_plate','product_id','designation_id','brand_id','emplacement_chantier_id','state_breakdown','capacity']})
        for engin in enginList:
            res.append({
                "id":engin.get("id",0),
                "name":engin['product_id'][1] if not isinstance(engin['product_id'],bool) else '',
                "plate":engin['license_plate'] if not isinstance(engin['license_plate'],bool) else '',
                "code":engin.get('code',''),
                "desc":engin['designation_id'][1] if not isinstance(engin['designation_id'],bool) else '',
                "brand":engin['brand_id'][1] if not isinstance(engin['brand_id'],bool) else '',
                "place":engin['emplacement_chantier_id'][1].capitalize() if not isinstance(engin['emplacement_chantier_id'],bool) else 'Indéfini',
                "state":engin.get('state_breakdown','').capitalize() if not isinstance(engin.get('state_breakdown',''),bool) else 'Indéfini',
                "capacity":engin.get('capacity','') if not isinstance(engin.get('capacity',''),bool) else 'Indéfini',
            })
        return res