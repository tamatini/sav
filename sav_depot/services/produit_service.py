from flask_restplus import Resource, Namespace, fields
from sav_depot.sav_model import Produit, Marque
from flask import request, jsonify
from sav_depot import db

api = Namespace('Produit', description='Les produits')

new_produit = api.model('new_produit', {
    'nom_produit': fields.String,
    'ean_produit': fields.String,
    'pv_produit': fields.String,
    'marque_produit': fields.String
})


@api.route('/')
class ProduitList(Resource):
    def get(self):
        return [{'nom_produit': c.nom_produit, 'ean_produit': c.ean_produit,
                 'pv_produit': c.pv_produit, 'marque_produit': c.marque_produit} for c in Produit.query.all()]

    @api.expect(new_produit)
    def post(self):
        nom_produit = request.json['nom_produit']
        ean_produit = request.json['ean_produit']
        pv_produit = request.json['pv_produit']
        marque_produit = request.json['marque_produit']
        if Produit.query.filter_by(nom_produit=nom_produit, ean_produit=ean_produit).first():
            return jsonify('Ce produit existe déjà')
        elif Marque.query.filter_by(marque_produit=marque_produit).first():
            marques = Marque.query.filter_by(marque_produit=marque_produit)
            marque_product = marques.marque_produit
            produit = Produit(nom_produit=nom_produit, ean_produit=ean_produit,
                              pv_produit=pv_produit, marque_produit=marque_product)
            db.session.add(produit)
            db.session.commit()
            return jsonify('le produit à été créer')
        else:
            marque = Marque(marque_produit=marque_produit)
            marques = Marque.query.filter_by(marque_produit=marque_produit)
            marque_product = marques.marque_produit
            produit = Produit(nom_produit=nom_produit, ean_produit=ean_produit,
                              pv_produit=pv_produit, marque_produit=marque_product)
            db.session.add(marque)
            db.session.add(produit)
            db.session.commit()
            return jsonify('La marque à été ajouter'), jsonify('Le produit à été rajouter')


@api.route('/'+'<string:produit_id>')
class ProduitDetail(Resource):
    def get(self, produit_id):
        return [{'Produit': c.nom_produit, 'ean': c.ean_produit, 'marque': c.marque_produit}
                for c in Produit.query.filter_by(nom_produit=produit_id)] or \
               [{'Produit': c.nom_produit, 'ean': c.ean_produit, 'marque': c.marque_produit}
                for c in Produit.query.filter_by(ean_produit=produit_id)]

    def delete(self, produit_id):
        if Produit.query.filter_by(nom_produit=produit_id):
            produit = Produit.query.filter_by(nom_produit=produit_id).first()
            produit_delete = produit.query.get(produit.produit_id)
            db.session.delete(produit_delete)
            db.session.commit()
            return jsonify('Le produit ' + produit_id + ' à été supprimer')
        else:
            return jsonify("Ce produit n'existe pas")



