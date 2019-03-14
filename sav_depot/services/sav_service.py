from flask_restplus import Resource, Namespace, fields
from sav_depot.sav_model import DepotSav, db
from flask import request, jsonify


api = Namespace('SAV', description='Les SAV')

new_produit = api.model('new_produit', {
    'nom_produit': fields.String,
    'date_achat': fields.String,
    'date_depot': fields.String,
})


@api.route('/')
class ProduitList(Resource):
    def get(self):
        return [{'nom_produit': c.nom_produit, 'ean_produit': c.ean_produit} for c in Produit.query.all()]

    @api.expect(new_produit)
    def post(self):
        nom_produit = request.json['nom_produit']
        ean_produit = request.json['ean_produit']
        pv_produit = request.json['pv_produit']
        marque_produit = request.json['marque_produit']
        if Produit.query.filter_by(nom_produit=nom_produit, ean_produit=ean_produit).first():
            return jsonify('Ce produit existe déjà')
        else:
            produit = Produit(nom_produit=nom_produit, ean_produit=ean_produit,
                              pv_produit=pv_produit, marque_produit=marque_produit)
            db.session.add(produit)
            db.session.commit()
        return jsonify('Le produit à bien été ajouter')


@api.route('/'+'<string:produit_id>')
class ProduitDetail(Resource):
    def get(self, produit_id):
        return [{'Produit': c.nom_produit, 'ean': c.ean_produit, 'marque': c.marque_produit}
                for c in Produit.query.filter_by(nom_produit=produit_id)] or \
               [{'Produit': c.nom_produit, 'ean': c.ean_produit, 'marque': c.marque_produit}
                for c in Produit.query.filter_by(ean_produit=produit_id)]

    def delete(self, prenom_id, nom_id):
        client = Produit.query.filter_by(nom_client=nom_id, prenom_client=prenom_id)
        db.session.delete(client)
        db.session.commit()

    @api.expect(new_produit)
    def put(self, produit_id):
        nom_produit = request.json['nom_produit']
        pv_produit = request.json['pv_produit']
        ean_produit = request.json['ean_produit']
        marque_produit = request.json['marque_produit']
        if Produit.query.filter_by(nom_produit=produit_id, ean_produit=produit_id).first():
            client_id = Produit.query.filter_by(nom_produit=produit_id, ean_produit=produit_id).first()
            client_id.nom_produit = nom_produit
            client_id.pv_produit = pv_produit
            client_id.ean_produit = ean_produit
            client_id.marque_produit = marque_produit
            db.session.commit()
            return [{'Produit': c.nom_produit, 'EAN': c.ean_produit, 'PV': c.pv_produit,
                    'Marque': c.marque_produit} for c in
                    Produit.query.filter_by(nom_produit=produit_id, ean_produit=produit_id)]
        else:
            return jsonify("Ce produit n'existe pas")



