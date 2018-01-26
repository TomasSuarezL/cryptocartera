from flask import Flask, render_template, request, url_for, jsonify

from models.models import User, db
import logging

logging.getLogger().setLevel(logging.DEBUG)
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user="ubuntu",pw="admin",url="127.0.0.1:5432",db="cryptocartera-test")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

logging.info(app.config['SQLALCHEMY_DATABASE_URI'])

with app.app_context():
    db.init_app(app)
    db.create_all()
    user1 = User(spotify_id="2", spotify_token="222")
    db.session.add(user1)
    db.session.commit()

    logging.info(User.query.all())




@app.route('/')
def main():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)