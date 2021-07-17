from functools import wraps
from flask_jwt_extended import (
    get_jwt_identity,
)
from application.models.userModel import UserModel
from application.om import OdooModel


def access_right_required(model,option='read'):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args,**kwargs):
            user_public_id = get_jwt_identity()
            user = UserModel.find_by_public_id(user_public_id)
            if OdooModel.check_access_rights(user,option,model) != True:
                return OdooModel.check_access_rights(user,option,model)
            else:
                return fn(*args, **kwargs)
        return decorator
    return wrapper