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
        return [{'nom_produit': c.nom_produit.capitalize(), 'ean_produit': c.ean_produit,
                 'pv_produit': str(c.pv_produit)+' Fcp', 'marque_produit': c.marque_produit.upper()}
                for c in Produit.query.all()]

    @api.expect(new_produit)
    def post(self):
        nom_produit = request.json['nom_produit']
        ean_produit = request.json['ean_produit']
        pv_produit = request.json['pv_produit']
        marque_produit = request.json['marque_produit']
        if Produit.query.filter_by(nom_produit=nom_produit.lower(), ean_produit=ean_produit).first():
            return jsonify('Ce produit existe déjà')
        else:
            produit = Produit(nom_produit=nom_produit.lower(), ean_produit=ean_produit,
                              pv_produit=pv_produit, marque_produit=marque_produit.lower())
            if Marque.query.filter_by(marque_produit=marque_produit.lower()).first():
                db.session.add(produit)
                db.session.commit()
                return jsonify('Cette marque existe déjà, le produit à été créer')

            else:
                marque = Marque(marque_produit=marque_produit.lower())
                db.session.add(marque, produit)
                db.session.commit()
        return jsonify('la marque et le produit ont été créer')


@api.route('/'+'<string:produit_id>')
class ProduitDetail(Resource):
    def get(self, produit_id):
        return [{'Produit': c.nom_produit.capitalize(), 'ean': c.ean_produit,
                 'pv_produit': str(c.pv_produit)+' Fcp', 'marque': c.marque_produit.upper()}
                for c in Produit.query.filter_by(nom_produit=produit_id.lower())] or \
               [{'Produit': c.nom_produit.capitalize(), 'ean': c.ean_produit,
                 'pv_produit': str(c.pv_produit)+' Fcp', 'marque': c.marque_produit.upper()}
                for c in Produit.query.filter_by(ean_produit=produit_id)]

    def delete(self, produit_id):
        if Produit.query.filter_by(ean_produit=produit_id).first():
            produit = Produit.query.filter_by(ean_produit=produit_id).first()
            produit_delete = produit.query.get(produit.produit_id)
            db.session.delete(produit_delete)
            db.session.commit()
        elif Produit.query.filter_by(nom_produit=produit_id).first():
            produit = Produit.query.filter_by(nom_produit=produit_id).first()
            produit_delete = produit.query.get(produit.produit_id)
            db.session.delete(produit_delete)
            db.session.commit()
        return jsonify('Le produit ' + produit.nom_produit.capitalize() + ' à été supprimer')

