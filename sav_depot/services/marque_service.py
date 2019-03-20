from flask_restplus import Resource, Namespace, fields
from sav_depot.sav_model import Marque, Produit
from flask import request, jsonify
from sav_depot import db

api = Namespace('Marque', description='Les marques de produit')


new_marque = api.model('new_marque', {
    'Marque': fields.String
})


@api.route('/')
class MarqueList(Resource):
    def get(self):
        return [{'Marque': c.marque_produit.upper()} for c in Marque.query.all()]

    @api.expect(new_marque)
    def post(self):
        nom_marque = request.json['Marque']
        if Marque.query.filter_by(marque_produit=nom_marque.lower()).first():
            return jsonify('Cette marque existe déjà')
        else:
            marque = Marque(marque_produit=nom_marque.lower())
            db.session.add(marque)
            db.session.commit()
        return jsonify('La marque ' + nom_marque.upper() + ' à été rajouter')


@api.route('/'+'<string:marque_id>')
class MarqueDetail(Resource):
    def get(self, marque_id):
        return [{'Marque': c.marque_produit.upper()} for c in
                Marque.query.filter_by(marque_produit=marque_id.lower())] and \
               [{'Produit': c.nom_produit.lower(), 'EAN': c.ean_produit, 'Prix': c.pv_produit + ' Fcp'}
                for c in Produit.query.filter_by(marque_produit=marque_id.lower())]

    def delete(self, marque_id):
        if Marque.query.filter_by(marque_produit=marque_id.lower()):
            marque = Marque.query.filter_by(marque_produit=marque_id.lower()).first()
            marque_delete = marque.query.get(marque.marque_id)
            db.session.delete(marque_delete)
            db.session.commit()
            return jsonify('La marque ' + marque_id.upper() + ' à été supprimer')
        else:
            return jsonify("Cette marque n'existe pas")
