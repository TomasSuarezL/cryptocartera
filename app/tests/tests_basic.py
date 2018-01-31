import os
import unittest
from datetime import datetime
from app.app import app
from app.models.models import db, User, CryptoOrden, Moneda, PrecioHistorico
from sqlalchemy import extract
 
 
class BasicTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user="ubuntu",pw="admin",url="127.0.0.1:5432",db="cryptocartera-test")
        self.app = app.test_client()
        with app.app_context():
            # db.drop_all()
            db.create_all()
            moneda = Moneda(moneda="BTC")
            db.session.add(moneda)
            db.session.commit()
 
 
    # executed after each test
    def tearDown(self):
        pass
 
 
###############
#### tests ####
###############
 
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        with app.app_context():
            user_test = User(spotify_id="123",spotify_token="123hjh123h5j")
            db.session.add(user_test)
            db.session.commit()

            get_user_test = User.query.filter_by(spotify_id="123").first()
            print get_user_test
        self.assertEqual(get_user_test.spotify_token,"123hjh123h5j")
 

    def test_create_crypto(self):
        with app.app_context():
            btc = Moneda.query.filter_by(moneda="BTC").first()

            new_crypto_test_with_BTC = CryptoOrden(ticker="ETH",cantidad=1, precio_compra_usd=1200.00,precio_compra=0.090050, moneda_compra=btc, fecha_compra=datetime(2018,1,27,16,5) )
            db.session.add(new_crypto_test_with_BTC)
            db.session.commit()

            get_new_crypto = CryptoOrden.query.filter_by(ticker="ETH").first()
        
        self.assertEqual(get_new_crypto.moneda_compra,btc)

    def test_create_precio_historico(self):
        with app.app_context():

            new_precio_historico = PrecioHistorico(ticker="ETH", precio = 1000, fecha=datetime.now())
            db.session.add(new_precio_historico)
            db.session.commit()

            get_precio_mes = PrecioHistorico.query.filter(extract('month',PrecioHistorico.fecha) == 1).first()

        self.assertEqual(get_precio_mes.precio,1000)

if __name__ == "__main__":
    unittest.main()