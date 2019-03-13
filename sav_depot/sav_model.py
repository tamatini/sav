from . import db
from datetime import date


class Client(db.Model):
    client_id = db.Column(db.Integer, primary_key=True)
    nom_client = db.Column(db.String(20), nullable=False, unique=False)
    prenom_client = db.Column(db.String(20), nullable=False, unique=False)
    tel_client = db.Column(db.String(20), nullable=False, unique=False)
    mail_client = db.Column(db.String(30), nullable=True, unique=False)


class Produit(db.Model):
    nom_produit = db.Column(db.String(20), nullable=False, unique=True, primary_key=True)
    marque_produit = db.Column(db.String(20), db.ForeignKey('marque.marque_id'), nullable=False)
    ean_produit = db.Column(db.Integer, nullable=False, unique=True)
    pv_produit = db.Column(db.Integer, nullable=False, unique=False)


class Marque(db.Model):
    marque_id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    marque_produit = db.Column(db.String(25), nullable=False, unique=True)


class DepotSav(db.Model):
    depot_id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    produit = db.Column(db.String, db.ForeignKey('produit.nom_produit'),
                        db.ForeignKey('produit.marque_produit'), nullable=True)
    date_depot = db.Column(db.DateTime, nullable=False, unique=False, default=date)
    date_achat = db.Column(db.DateTime, nullable=False, unique=False)

