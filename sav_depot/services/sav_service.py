from flask_restplus import Resource, Namespace, fields
from sav_depot.sav_model import DepotSav, Client, Marque, Produit, Magasin
from flask import request, jsonify
from sav_depot import db
api = Namespace('SAV', description='Les dépots SAV')

new_depot = api.model('new_depot', {
    'date_achat': fields.String,
    'date_depot': fields.String
})


@api.route('/')
class ProduitList(Resource):
    def get(self):
        return [{'nom_client': c.nom_client, 'prenom_client': c.prenom_client, 'sav': c.sav}
                for c in Client.query.all()]


@api.route('/'+'<string:nom_client>'+' '+'<string:prenom_client>'+' '+'<string:produit_id>')
class SavDetail(Resource):
    def get(self, nom_client, prenom_client):
        return [{'Nom client': c.nom_client, 'Prenom client': c.prenom_client, 'SAV': c.sav}
                for c in DepotSav.query.filter_by(nom_client=nom_client, prenom_client=prenom_client)]

    @api.expect(new_depot)
    def post(self, nom_client, prenom_client, produit_id):
        date_achat = request.json['date_achat']
        date_depot = request.json['date_depot']
        if Client.query.filter_by(nom_client=nom_client.lower(), prenom_client=prenom_client.lower()).first():
            depot_sav = DepotSav(date_achat=date_achat, date_depot=date_depot)
            if Produit.query.filter_by(ean_produit=produit_id).first():
                produit = Produit.query.filter_by(ean_produit=produit_id).first()
                produit_id = produit.query.get(produit.produit_id)
            elif Produit.query.filter_by(nom_produit=produit_id).first():
                produit = Produit.query.filter_by(nom_produit=produit_id).first()
                produit_id = produit.query.get(produit.produit_id)
            depot_sav = DepotSav()
            db.session.add(depot_sav)
            db.session.commit()
            return jsonify('Le sav a été enregistrer')
        else:
            return jsonify("Ce client n'existe pas")


@api.route('/'+'<string:nom_client>'+' '+'<string:prenom_client>'+' '+'<string:sav_id>')
class DepotSav(Resource):
   def get(self, nom_client, prenom_client, sav_id):
        return [{'Nom client': c.nom_client, 'Prenom client': c.prenom_client, 'SAV': c.sav}
                for c in Client.query.filter_by(nom_client=nom_client, prenom_client=prenom_client,sav=sav_id)]


