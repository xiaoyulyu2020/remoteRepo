from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
'''
    flask db init
    flask db migrate
    flask db upgrade
'''
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mymainuser:mypassword@db/main'
CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)

    UniqueConstraint('user_id', 'product_id', name='user_product_id')
@app.route('/')
def index():
    return 'Hello World!'
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)