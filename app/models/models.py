from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(200), unique=False, nullable=True)
    spotify_token = db.Column(db.String(200), unique=False, nullable=True)


class CryptoOrden(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(7))
    cantidad = db.Column(db.Float)
    precio_compra_usd = db.Column(db.Float)
    precio_compra = db.Column(db.Float)
    moneda_compra_id = db.Column(db.Integer, db.ForeignKey("moneda.id"), nullable=False)
    moneda_compra = db.relationship('Moneda',backref="cryptoorden", lazy='subquery')
    fecha_compra = db.Column(db.DateTime)

    def to_json(self):
        return {
        "ticker": self.ticker,
        "cantidad": self.cantidad,
        "precio_compra_usd": self.precio_compra_usd,
        "precio_compra": self.precio_compra,
        "moneda_compra": self.moneda_compra.moneda,
        "fecha_compra": self.fecha_compra
    }

class Moneda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    moneda = db.Column(db.String(10))


class PrecioHistorico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(7))
    precio = db.Column(db.Float)
    fecha = db.Column(db.DateTime)
