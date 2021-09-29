
class InvalidUsage(Exception):
    status_code = 401

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        
        if status_code is not None:
            self.status_code = status_code
        elif 'Errno 111' in message:
            self.status_code = 503
            self.message = "Service blocké ou serveur non disponible veuillez réessayer plus tard"
        elif 'été supprimé ' in message:
            self.status_code = 404
            self.message = "L'un des documents que vous voulez accéder a été supprimé ou n'existe plus"
        elif 'mandatory field is not correctly set' in message:
            self.status_code = 400
            self.message = "Request mal formé veuillez verifier le champs " + message.split(":")[len(message.split(":"))-1].replace(']\'>','')
        elif 'Fault' in message:
            self.status_code = 500
            self.message = "Erreur interne " + message.split(":")[len(message.split(":"))-1].replace(']\'>','')
        
        self.message = message
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['msg'] = self.message
        return rv
