from flask_restplus import Resource, Namespace
from sav_depot.sav_model import Client


api = Namespace('Client', description='les clients')
client_list = [{'nom': 'TEAHUI', 'prenom': 'Tamatini', 'n°tel': '87 44 44 44'}]


@api.route('/')
class ClientList(Resource):
    def get(self):
       return [{'Nom': c.nom_client, 'Prenom': c.prenom_client, 'Tel': c.tel_client, 'Mail': c.mail_client} for c in Client.query.all()]


@api.route('/'+'<string:client_id>')
class ClientDetail(Resource):
    def get(self, client_id):
        nom = Client.query.filter_by(nom_client=client_id)
        prenom = Client.query.filter_by(prenom_client=client_id)
        return [{'Nom': c.nom_client,
                 'Prénom': c.prenom_client} for c in nom] + [{'Nom': c.nom_client, 'Prénom': c.prenom_client} for c in prenom]
