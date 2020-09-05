import sys
sys.path.append("c:\\Users\\rdhavade\\OneDrive\\OneDrive - Cisco\\working_directory\\FoodApp\\FoodAPI")
sys.path.append("..")
from api import *
from flask import Flask 
from flask_restful import abort, Api, fields, marshal_with, reqparse, Resource 
from datetime import datetime 
from models import RestaurantModel 
import status 
from pytz import utc
from user_api import *

#CREATING API
app = Flask(__name__) 
api = Api(app)

#RESTAURANT API
api.add_resource(RestaurantList, '/api/restaurants/')
api.add_resource(Restaurant, '/api/restaurants/<int:id>', endpoint='message_endpoint')

#USER API
api.add_resource(UserList, '/api/users/')
api.add_resource(User, '/api/users/<int:id>', endpoint='user_endpoint')
api.add_resource(check_username,'/api/users/check_username')
api.add_resource(validate_username,'/api/users/validate_username')

if __name__ == '__main__':
    app.run(debug=True)
