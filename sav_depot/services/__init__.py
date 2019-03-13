from flask_restplus import Api
from .client_service import api as client_api
from .marque_service import api as marque_api

api = Api(title='sav', description='commande relative au client')
api.add_namespace(client_api)
api.add_namespace(marque_api)


