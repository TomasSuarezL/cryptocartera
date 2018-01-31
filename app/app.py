from flask import Flask, render_template, request, url_for, jsonify
from datetime import datetime
from models.models import Moneda, CryptoOrden, db
import logging

logging.getLogger().setLevel(logging.DEBUG)
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user="ubuntu",pw="admin",url="127.0.0.1:5432",db="cryptocartera-test")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

logging.info(app.config['SQLALCHEMY_DATABASE_URI'])

with app.app_context():
    db.init_app(app)
    db.create_all()


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/api/crypto', methods=['GET','POST'])
def cryptos():
    if request.method == 'POST':

        moneda = Moneda.query.filter_by(moneda=request.form['moneda']).first()

        new_crypto = CryptoOrden(ticker=request.form['ticker'],
         cantidad=request.form['cantidad'],
         precio_compra_usd=request.form['precio'],
         precio_compra=request.form['precio_moneda'], 
         moneda_compra=moneda,
         fecha_compra=datetime.strptime(request.form['fecha'], '%d/%m/%Y %H:%M') )
        
        db.session.add(new_crypto)
        db.session.commit()

        print new_crypto
        return jsonify(request.form)
    else:
        cryptosArr = []
        cryptos = CryptoOrden.query.all()
        for c in cryptos:
            cryptosArr.append(c.to_json())
        return jsonify(cryptosArr)


@app.route('/api/savedata')
def saveData():
    return "OK"


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)