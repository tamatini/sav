from flask_restplus import Api
from .client_service import api as client_api
from .marque_service import api as marque_api
from .produit_service import api as produit_api
from .sav_service import api as sav_api


# description de l'API principal
api = Api(
    title='sav',
    version='1,0',
    description='Logiciel de gestion des retours SAV')


# intégration des différent services
api.add_namespace(client_api)
api.add_namespace(marque_api)
api.add_namespace(produit_api)
api.add_namespace(sav_api)

