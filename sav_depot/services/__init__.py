from flask_restplus import Api, fields
from .client_service import api as client_api


api = Api(title='sav', description='commande relative au client')
api.add_namespace(client_api)


