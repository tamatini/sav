from flask_restplus import Resource, Namespace, fields
from sav_depot.sav_model import Marque, db
from flask import request, jsonify

api = Namespace('Marque', description='Les marques de produit')


new_marque = api.model('new_marque', {
    'nom_marque': fields.String
})


@api.route('/')
class MarqueList(Resource):
    def get(self):
        return [{'marque': c.marque_produit} for c in Marque.query.all()]

    @api.expect(new_marque)
    def post(self):
        nom_marque = request.json['nom_marque']
        if Marque.query.filter_by(marque_produit=nom_marque).first():
            return jsonify('Cette marque existe déjà')
        else:
            marque = Marque(marque_produit=nom_marque)
            db.session.add(marque)
            db.session.commit()
        return jsonify('La marque'+' '+nom_marque+' '+'à été rajouter')

