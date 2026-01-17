from dataclasses import dataclass
from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import UniqueConstraint
import requests
from producer import publish

# from producer import publish

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'
CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))


@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')




@app.route('/')
def home():
    return 'Hello from Products Microservice!'

@app.route('/api/products')
def index():
    return jsonify(Product.query.all())


@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    try:
        req = requests.get('http://host.docker.internal:8000/api/user')
        req.raise_for_status()  # Raise exception for bad status codes
        json = req.json()
    except requests.exceptions.RequestException as e:
        abort(500, f'Failed to fetch user data: {str(e)}')
    except ValueError:
        abort(500, 'Invalid JSON response from user service')

    try:
        productUser = ProductUser(user_id=json['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()

        publish('product_liked', id)
    except:
        abort(400, 'You already liked this product')

    return jsonify({
        'message': 'success'
    })


@app.route('/api/products/<int:id>')
def get_product(id):
    product = Product.query.get(id)
    if not product:
        abort(404, 'Product not found')
    return jsonify(product)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
