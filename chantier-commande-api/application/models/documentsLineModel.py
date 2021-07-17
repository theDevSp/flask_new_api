class DocumentsLineModel():

    def __init__(self,product,qty,vehicle_id,note,created_by=None,create_date=None,write_date=None,id=None):

        self.id = id
        self.product = product
        self.qty = qty
        self.note = note
        self.vehicle_id = vehicle_id
        self.created_by = created_by
        self.create_date = create_date
        self.write_date = write_date