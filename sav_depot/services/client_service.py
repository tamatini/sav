from flask_restplus import Resource, Namespace, fields
from sav_depot.sav_model import Client
from flask import request, jsonify
from sav_depot import db

api = Namespace('Client', description='Les clients')

new_client = api.model('new_client', {
    'Nom': fields.String,
    'Prénom': fields.String,
    'Tel': fields.String,
    'Mail': fields.String
})

update_client = api.model('update_client', {
    'tel': fields.String,
    'mail': fields.String
})


@api.route('/')
class ClientList(Resource):
    def get(self):
        client = [{'ID': c.client_id, 'Nom': c.nom_client.upper(), 'Prénom': c.prenom_client.capitalize()}
                  for c in Client.query.all()]
        return client

    @api.expect(new_client)
    def post(self):
        nom = request.json['Nom']
        prenom = request.json['Prénom']
        tel = request.json['Tel']
        mail = request.json['Mail']
        if Client.query.filter_by(nom_client=nom.lower(), prenom_client=prenom.lower()).first():
            return jsonify('Ce client est déjà enregistrer')
        else:
            client = Client(nom_client=nom.lower(), prenom_client=prenom.lower(), tel_client=tel, mail_client=mail)
            db.session.add(client)
            db.session.commit()
        return jsonify('Le client '+nom + ' ' + prenom + ' à bien été créer')


@api.route('/'+'<string:nom_id>'+' '+'<string:prenom_id>')
class ClientDetail(Resource):
    def get(self, prenom_id, nom_id):
        return [{'Nom': c.nom_client.upper(), 'Prénom': c.prenom_client.capitalize(),
                 'Tel': c.tel_client, 'Mail': c.mail_client}
                for c in Client.query.filter_by(nom_client=nom_id.lower(), prenom_client=prenom_id.lower())]

    def delete(self, prenom_id, nom_id):
        if Client.query.filter_by(nom_client=nom_id.lower(), prenom_client=prenom_id.lower()).first():
            client = Client.query.filter_by(nom_client=nom_id.lower(), prenom_client=prenom_id.lower()).first()
            client_delete = client.query.get(client.client_id)
            db.session.delete(client_delete)
            db.session.commit()
            return jsonify('Le client ' + nom_id.upper() + ' ' + prenom_id.capitalize() + ' à été supprimer')
        else:
            return jsonify('Le client ' + nom_id.upper() + ' ' + prenom_id.capitalize() + " n'est plus dans la liste")

    @api.expect(update_client)
    def put(self, prenom_id, nom_id):
        tel = request.json['Tel']
        mail = request.json['Mail']
        if Client.query.filter_by(nom_client=nom_id.lower(), prenom_client=prenom_id.lower()).first():
            client_id = Client.query.filter_by(nom_client=nom_id.lower(), prenom_client=prenom_id.lower()).first()
            client_id.tel_client = tel
            client_id.mail_client = mail
            db.session.commit()
            return [{'Nom': c.nom_client, 'Prénom': c.prenom_client, 'Tel': c.tel_client,
                    'Mail': c.mail_client} for c in
                    Client.query.filter_by(nom_client=nom_id, prenom_client=prenom_id)]
        else:
            return jsonify("Ce client n'existe pas dans la base de données")



