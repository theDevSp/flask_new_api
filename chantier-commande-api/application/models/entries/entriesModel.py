import datetime
from application.ressources.errors import InvalidUsage

from application.om import OdooModel as om 

import sys

engin = om.ENGIN

class EntriesModel:

    _model_moves = ['stock.external.move']

    def __init__(self, product_id, product, obs,unit,product_ref,product_int_ref,qty,source):
        
        
        self.product_id = product_id
        self.product = product
        self.obs = obs
        self.unit = unit
        self.product_ref = product_ref
        self.product_int_ref = product_int_ref
        self.qty = qty
        self.source = source
     
    def __str__(self) -> str:
        return f"{self.product}"
    
    @classmethod
    def get_entries_by_ch_period(cls,ch_id,year,month,user):
        
        res = result_set = [] 
        if om.check_access_rights(user,'create',*cls._model_moves) != True:
            raise InvalidUsage(str(om.check_access_rights(user,'read',*cls._model_moves)), status_code=410)
        
        try:
            query = """ 
                        select sm.product_id,
                        pt.name as product,
                        pu.name as unit,
                        case  when pt.product_brand_ref is null then '' else pt.product_brand_ref end as product_ref,
                        case  when pt.default_code is null then '' else pt.default_code end as product_int_ref,
                        CAST(max(sm.date_expected) as varchar) as date,
                        case  when min(sm.origin) is null then 'm' else 'F' end as from,
                        

                        CAST(ROUND(sum(sm.product_qty),3) as float) - COALESCE((select 
                            CAST(ROUND(sum(smout.product_qty),3) as float)
                            from stock_move smout

                            where smout.state in ('done')
                            and smout.location_id = (select location_id from fleet_vehicle_chantier where id =%s)
                            and smout.vehicle_id = 3684
                            and  ( smout.date_expected between '%s' and '%s' )
                            and smout.product_id = sm.product_id
                            group by smout.product_id
                            ),0) as qty,
                        
                        COALESCE((select 
                            CAST(ROUND(sum(smprevu.product_qty),3) as float)
                            from stock_move smprevu

                            where smprevu.state in ('assigned')	
                            and smprevu.location_dest_id = (select location_id from fleet_vehicle_chantier where id =%s)
                            and smprevu.vehicle_id = 3684
                            and  ( smprevu.date_expected between '%s' and '%s' )
                            
                            and smprevu.product_id = sm.product_id
                            group by smprevu.product_id
                            ),0) as qty_prevu

                        from stock_move sm
                        left join product_template pt
                        on pt.id = (select product_tmpl_id from product_product where id = sm.product_id)
                        left join product_uom pu
                        on pu.id = sm.product_uom

                        where sm.location_dest_id = (select location_id from fleet_vehicle_chantier where id =%s)
                        and sm.vehicle_id = 3684
                        and ( sm.date_expected between '%s' and '%s' )
                        and  sm.state in ('done')
                    
                        group by 
                            sm.product_id,
                            pt.name,
                            pt.product_brand_ref,
                            pt.default_code,
                            pu.name
                        order by 2;""" % (ch_id,year+'/'+month+'/1',year+'/'+month+'/'+cls.num_to_month(mon=month,year=year),ch_id,year+'/'+month+'/1',year+'/'+month+'/'+cls.num_to_month(mon=month,year=year),ch_id,year+'/'+month+'/1',year+'/'+month+'/'+cls.num_to_month(mon=month,year=year))
            

            result_set = engin.execute(query)  
        except Exception: 
            raise InvalidUsage(str(sys.exc_info()[1]))
        if result_set:
            
            for ins in result_set.mappings().all() :
                temp_dict = {}
                if ins['qty'] > 0 or ins['qty_prevu'] > 0:
                    for key in ins:
                        temp_dict[key] = ins[key]
                        temp_dict['ch_id'] = ch_id
                        
                        temp_dict['cmd'] = cls.get_origin_bce_by_cumul_product(ins['product_id'],ch_id,year,month,user)
                    res.append(temp_dict)
        
        return res
    
    @classmethod
    def get_entries_by_product_period(cls,product_id,ch_id,year,month,user):
        res = result_set = [] 
        if om.check_access_rights(user,'read',*cls._model_moves) != True:
            raise InvalidUsage(str(om.check_access_rights(user,'read',*cls._model_moves)), status_code=410)

        try:
            query = """select
                        sm.id,
                        sm.product_id,
                        pt.name as product,
                        pu.name as unit,
                        sm.name as obs,
                        
                        
                        case  when rp.name is null then '' else rp.name end as partner,
                        case  when pt.product_brand_ref is null then '' else pt.product_brand_ref end as product_ref,
                        case  when pt.default_code is null then '' else pt.default_code end as product_int_ref,
                        CAST(sm.date_expected as varchar) as date,
                        CAST(ROUND(sm.product_qty,3) as float) - COALESCE ((select CAST(ROUND(sum(smout.product_qty),3) as float) 
							from stock_move smout
							where smout.origin_returned_move_id = sm.id
							group by smout.product_id),0) as qty,
                        
						
                        case  when sm.state ='done' then 'Recu' else 'Prévu' end as statu,
						case  when min(sm.origin) is null then 'm' else 'F' end as from,
                        max(sp.name)  doc,
                        max(sp.bce_chantier) bceId,
                        max(sem.name) bceName
                        from stock_move sm
                        left join product_template pt
                        on pt.id = (select product_tmpl_id from product_product where id = sm.product_id)
                        left join product_uom pu
                        on pu.id = sm.product_uom
                        left join res_partner rp
                        on rp.id = (select partner_id from stock_picking where id = sm.picking_id)
                        left join stock_picking sp
						on sm.picking_id = sp.id
                        left join stock_external_move sem
                        on sem.id = sp.bce_chantier
                        where sm.state in ('done','assigned')
                        and sm.product_id = %s
                        and sm.location_dest_id = (select location_id from fleet_vehicle_chantier where id =%s)
                        and sm.vehicle_id = 3684
                        and  ( sm.date_expected between '%s' and '%s' )

                        group by
                            sm.id,
                            sm.product_id,
                            pt.name,
                            pt.product_brand_ref,
                            pt.default_code,
                            pu.name,
                            sm.name,
                            sm.date_expected,
                            sm.product_qty,
                            sm.state,
                            rp.name
                        order by 1;""" % (product_id,ch_id,year+'/'+month+'/1',year+'/'+month+'/'+cls.num_to_month(mon=month,year=year)) 

        
            result_set = engin.execute(query) 
        except Exception: 
            raise InvalidUsage(str(sys.exc_info()[1]))
        if result_set:
            
            for ins in result_set.mappings().all() :
                temp_dict = {}
                if ins['qty'] > 0 or ins['qty_prevu'] > 0:
                    for key in ins:
                        temp_dict[key] = ins[key]
                        if ins['from'] == 'm':
                            temp_dict['partner'] = 'Stock/Magasin'
                        temp_dict['ch_id'] = int(ch_id)
                    res.append(temp_dict)
        
        return res
    
    @classmethod
    def get_origin_bce_by_cumul_product(cls,product_id,ch_id,year,month,user):
        res = result_set = [] 
        if om.check_access_rights(user,'read',*cls._model_moves) != True:
            raise InvalidUsage(str(om.check_access_rights(user,'read',*cls._model_moves)), status_code=410)
        try:
            query = """
                    select id,name
                    from stock_external_move sem 
                    where id in (select bce_chantier 
                                    from stock_picking sp
                                    where id in (
                                        select picking_id 
                                        from stock_move sm 
                                        where sm.state in ('done','assigned')
                                        and sm.product_id = %s
                                        and sm.location_dest_id = (select location_id from fleet_vehicle_chantier where id =%s)
                                        and sm.vehicle_id = 3684
                                        and  ( sm.date_expected between '%s' and '%s' )
                                    ))
            """ % (product_id,ch_id,year+'/'+month+'/1',year+'/'+month+'/'+cls.num_to_month(mon=month,year=year)) 

        
            result_set = engin.execute(query) 
        except Exception: 
            raise InvalidUsage(str(sys.exc_info()[1]))
        if result_set:
            for bces in result_set.mappings().all() :
                temp_dict = {}
                    
                for key in bces:
                    temp_dict[key] = bces[key]
                res.append(temp_dict)
        return res
    @classmethod
    def num_to_month(*args, **kwargs):

        month = kwargs.get("mon", None)
        year = kwargs.get("year", None)

        feb = '28'
        if((int(year) % 400 == 0) or (int(year) % 100 != 0) and(int(year) % 4 == 0)):
            feb = '29'

        if int(month) <= 12 and int(month) > 0:

            list_of_months = {'1': '31', '2': feb, '3': '31',
                              '4': '30', '5': '31', '6': '30', '7': '31',
                              '8': '31', '9': '30', '10': '31',
                              '11': '30', '12': '31'}

            return list_of_months[month]