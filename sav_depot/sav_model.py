from sav_depot import db
from datetime import date


class Client(db.Model):
    db.__tablename__ = "client"
    client_id = db.Column(db.Integer, primary_key=True)
    nom_client = db.Column(db.String(20), nullable=False, unique=False)
    prenom_client = db.Column(db.String(20), nullable=False, unique=False)
    tel_client = db.Column(db.String(20), nullable=False, unique=False)
    mail_client = db.Column(db.String(30), nullable=True, unique=False)
    sav = db.relationship("DepotSav", backref="depotsav")

    def __repr__(self):
        return f"Client('{self.client_id}''{self.nom_client}, '{self.prenom_client}', " \
            f"{self.tel_client}', '{self.mail_client}')"


class Produit(db.Model):
    db.__tablename__ = "produit"
    produit_id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    nom_produit = db.Column(db.String(20), nullable=False, unique=True)
    marque_produit = db.Column(db.String(20), db.ForeignKey('marque.marque_produit'), nullable=False)
    ean_produit = db.Column(db.Integer, nullable=False, unique=True)
    pv_produit = db.Column(db.Integer, nullable=False, unique=False)

    def __repr__(self):
        return f"Produit('{self.nom_produit}, '{self.marque_produit}', {self.ean_produit}', '{self.pv_produit}')"


class Marque(db.Model):
    db.__tablename__ = "marque"
    marque_id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    marque_produit = db.Column(db.String(25), nullable=False, unique=True)
    produits = db.relationship("Produit", backref="produit")

    def __repr__(self):
        return f"Marque('{self.marque_produit}, '{self.produits}')"


class DepotSav(db.Model):
    db.__tablename__ = "depotsav"
    depot_id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))
    produit = db.Column(db.String(50), db.ForeignKey('produit.nom_produit'), nullable=True)
    date_depot = db.Column(db.DateTime, nullable=False, unique=False, default=date)
    date_achat = db.Column(db.DateTime, nullable=False, unique=False)
    magasin = db.Column(db.Integer, db.ForeignKey('magasin.magasin_id'))
    situation = db.Column(db.Integer, db.ForeignKey('situation.situation'), nullable=False)

    def __repr__(self):
        return f"DepotSav('{self.produit}', {self.date_depot}', '{self.date_achat}', '{self.magasin}')"


class Magasin(db.Model):
    db.__tablename__ = "magasin"
    magasin_id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    nom_magasin = db.Column(db.String(30), nullable=False, unique=True)

    def __repr__(self):
        return f"Magasin('{self.nom_magasin}')"


class Situation(db.Model):
    db.__tablename__ = "Situation"
    situation_id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    situation = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return f"Magasin('{self.situation}')"

