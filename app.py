# For reading Heroku environmenet variables
import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

# For CORS 
from flask_cors import CORS

app = Flask(__name__)
# This will enable request from each origin
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Item that has been change but not added in database. SQL_Alchemy has advance tracker that is why we are turning it off
app.secret_key = 'This is my secret key please don\'t share it '
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__': 
    from db import db   # We are importing it here because of circular depenedencies
    db.init_app(app)   
    app.run(port=5000, debug=True)