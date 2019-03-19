from flask_restplus import Resource, Namespace, fields
from sav_depot.sav_model import Client
from flask import request, jsonify
from sav_depot import db
api = Namespace('SAV', description='Les dépots SAV')

new_depot = api.model('new_depot', {
    'client_id': fields.String,
    'nom_produit': fields.String,
    'ean_produit': fields.String,
    'marque_produit': fields.String,
    'date_achat': fields.String,
    'date_depot': fields.String
})


@api.route('/')
class ProduitList(Resource):
    def get(self):
        return [{'nom_client': c.nom_client, 'prenom_client': c.prenom_client, 'sav': c.sav}
                for c in Client.query.all()]


@api.route('/'+'<string:nom_client>'+' '+'<string:prenom_client>')
class SavDetail(Resource):
    def get(self, nom_client, prenom_client):
        return [{'Nom client': c.nom_client, 'Prenom client': c.prenom_client, 'SAV': c.sav}
                for c in Client.query.filter_by(nom_client=nom_client, prenom_client=prenom_client)]

    """"@api.expect(new_depot)
    def post(self, nom_client, prenom_client):
        nom_produit = request.json['nom_produit']
        ean_produit = request.json['ean_produit']
        pv_produit = request.json['pv_produit']
        marque_produit = request.json['marque_produit']
        if (nom_client, prenom_client) != \
                Client.query.filter_by(nom_client=nom_client, prenom_client=prenom_client).first():
            return jsonify("Ce client n'existe pas")
        else:
            sav = DepotSav(nom_produit=nom_produit, ean_produit=ean_produit,
                              pv_produit=pv_produit, marque_produit=marque_produit)
            db.session.add(sav)
            db.session.commit()
        return jsonify('Le produit à bien été ajouter')"""


@api.route('/'+'<string:nom_client>'+' '+'<string:prenom_client>'+' '+'<string:sav_id>')
class ClientSavDetail(Resource):
    def get(self, nom_client, prenom_client, sav_id):
        return [{'Nom client': c.nom_client, 'Prenom client': c.prenom_client, 'SAV': c.sav}
                for c in Client.query.filter_by(nom_client=nom_client, prenom_client=prenom_client, sav=sav_id)]
