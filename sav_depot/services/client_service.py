from flask_restplus import Resource, Namespace, fields
from sav_depot.sav_model import Client, db
from flask import request


api = Namespace('Client', description='les clients')
new_client = api.model('Client', {
    'nom': fields.String,
    'prenom': fields.String,
    'tel': fields.String,
    'mail': fields.String
})


@api.route('/')
class ClientList(Resource):
    def get(self):
        return [{'Nom': c.nom_client, 'Prenom': c.prenom_client} for c in Client.query.all()]

    @api.expect(new_client)
    def put(self):
        nom = request.json['nom']
        prenom = request.json['prenom']
        tel = request.json['tel']
        mail = request.json['mail']
        client = Client(nom_client=nom, prenom_client=prenom, tel_client=tel, mail_client=mail)
        db.session.add(client)
        db.session.commit()



@api.route('/'+'<string:client_id>')
class ClientDetail(Resource):
    def get(self, client_id):
        nom = Client.query.filter_by(nom_client=client_id)
        prenom = Client.query.filter_by(prenom_client=client_id)
        return [{'Nom': c.nom_client, 'Prénom': c.prenom_client} for c in nom] or \
               [{'Nom': c.nom_client, 'Prénom': c.prenom_client} for c in prenom]
