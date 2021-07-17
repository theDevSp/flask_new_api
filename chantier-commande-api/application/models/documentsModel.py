
class DocumentsModel():

    def __init__(self,name,demandeur,ch_id,note,created_by=None,create_date=None,write_date=None,id=None,state=''):

        self.id = id
        self.name = name
        self.demandeur = demandeur
        self.note = note
        self.ch_id = ch_id
        self.created_by = created_by
        self.create_date = create_date
        self.write_date = write_date
        self.state = state