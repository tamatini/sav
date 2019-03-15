from flask_restplus import Resource, Namespace, fields
from sav_depot.sav_model import Client, DepotSav, Magasin, Marque, Situation, db
from flask import request, jsonify


api = Namespace('Client', description='Les clients')

new_client = api.model('new_client', {
    'nom': fields.String,
    'prenom': fields.String,
    'tel': fields.String,
    'mail': fields.String
})

update_client = api.model('update_client', {
    'tel': fields.String,
    'mail': fields.String
})


@api.route('/')
class ClientList(Resource):
    def get(self):
        return [{'ID': c.client_id, 'Nom': c.nom_client, 'Prenom': c.prenom_client} for c in Client.query.all()]

    @api.expect(new_client)
    def post(self):
        nom = request.json['nom']
        prenom = request.json['prenom']
        tel = request.json['tel']
        mail = request.json['mail']
        if Client.query.filter_by(nom_client=nom, prenom_client=prenom).first():
            return jsonify('Ce client est déjà enregistrer')
        else:
            client = Client(nom_client=nom, prenom_client=prenom, tel_client=tel, mail_client=mail)
            db.session.add(client)
            db.session.commit()
        return jsonify('Le client '+nom + ' ' + prenom + ' à bien été créer')


@api.route('/'+'<string:nom_id>'+' '+'<string:prenom_id>')
class ClientDetail(Resource):
    def get(self, prenom_id, nom_id):
        return [{'nom': c.nom_client, 'prenom': c.prenom_client, 'tel': c.tel_client, 'mail': c.mail_client}
                for c in Client.query.filter_by(nom_client=nom_id, prenom_client=prenom_id)]

    def delete(self, prenom_id, nom_id):
        client = Client.query.filter_by(nom_client=nom_id, prenom_client=prenom_id)
        db.session.delete(client)
        db.session.commit()

    @api.expect(update_client)
    def put(self, prenom_id, nom_id):
        tel = request.json['tel']
        mail = request.json['mail']
        if Client.query.filter_by(nom_client=nom_id, prenom_client=prenom_id).first():
            client_id = Client.query.filter_by(nom_client=nom_id, prenom_client=prenom_id).first()
            client_id.tel_client = tel
            client_id.mail_client = mail
            db.session.commit()
            return [{'Nom': c.nom_client, 'Prénom': c.prenom_client, 'tel': c.tel_client,
                    'mail': c.mail_client} for c in
                    Client.query.filter_by(nom_client=nom_id, prenom_client=prenom_id)]
        else:
            return jsonify("Ce client n'existe pas dans la base de données")



