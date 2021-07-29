
from flask import Flask, json,jsonify
from dotenv import load_dotenv
from application.config import configurations as cfg
from flask_restful import Api
from flask_jwt_extended import JWTManager


from application.db import db
from application.ma import ma

from werkzeug.exceptions import *
from application.ressources.errors import InvalidUsage
               
    


def init_app():
    app = Flask(__name__)
    load_dotenv(".env")
    app.config.from_object(cfg['development'])
    

    db.init_app(app)
    ma.init_app(app)
    api = Api(app)
    @app.before_first_request
    def create_tables():
        db.create_all()


    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response

    jwt = JWTManager(app)
    with app.app_context():
        from application.ressources.userResource import UserLogin,User
        from application.ressources.chantierResource import ChantierResource
        from application.ressources.enginResource import EnginResource
        from application.ressources.employeeResource import EmployeeResource
        from application.ressources.numPrixResource import NumPrixResource
        from application.ressources.responsbleResource import ResponsableResource
        from application.ressources.commande.bceResource import BceResource
        from application.ressources.commande.bceLineResource import BceLineResource
        from application.ressources.add_attribution import add
        api.add_resource(UserLogin, "/login")
        api.add_resource(User, "/user")
        api.add_resource(ChantierResource, "/chantier")
        api.add_resource(EnginResource, "/gmao")
        api.add_resource(EmployeeResource, "/employee")
        api.add_resource(ResponsableResource, "/responsable")
        api.add_resource(NumPrixResource, "/num_price")

        api.add_resource(BceResource, "/commande",endpoint='create-get')
        api.add_resource(BceResource, "/commande/<int:bce_id>",endpoint='update-delete')
        api.add_resource(BceLineResource, "/commande_line",endpoint='create-get-line')
        api.add_resource(BceLineResource, "/commande_line/<int:bce_line_id>",endpoint='update-delete-line')
        api.add_resource(add, "/attribution")

        return app
    
