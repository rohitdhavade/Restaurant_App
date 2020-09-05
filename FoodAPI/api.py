from flask import Flask 
from flask_restful import abort, Api, fields, marshal_with, reqparse, Resource 
from datetime import datetime 
from models import RestaurantModel 
import status 
from pytz import utc

def write_to_file(file_name:str,content:str):
    with open(file_name,'a') as outfileh:
        outfileh.write(content)

write_to_file('api-logs.txt','started code\n')

# Below class ModelManager is used to manage our resource with add, get, delete methods.
# these methods may operate with the database like, SQL to perform the required actions i.e. add, get, delete etc.
class ModelManager():
    last_id = 0
    def __init__(self):
        write_to_file('api-logs.txt','inside class ModelManager __init__\n')
        self.restaurants = {} # dictionary of RestaurantModel class instances
        write_to_file('api-logs.txt','  value of restaurants dict is : ' + str(self.restaurants))
    def add_restaurant(self, restaurant:RestaurantModel):
        write_to_file('api-logs.txt','inside class ModelManager add_restaurant()\n')
        self.__class__.last_id += 1
        restaurant.id = self.__class__.last_id
        write_to_file('api-logs.txt','  value of restaurant.id is : ' + str(restaurant.id) + '\n')
        write_to_file('api-logs.txt','  value of restaurant is : ' + str(restaurant)+ '\n')
        self.restaurants[self.__class__.last_id] = restaurant
    def get_restaurant(self, id):
        write_to_file('api-logs.txt','inside class ModelManager get_restaurant()\n')
        write_to_file('api-logs.txt','  value of id is : ' + str(id) + '\n')
        return self.restaurants[id] # returns an instance of RestaurantModel class with given id
 
    def delete_restaurant(self, id): 
        write_to_file('api-logs.txt','inside class ModelManager delete_restaurant\n')
        write_to_file('api-logs.txt','  value of message is : ' + str(self.restaurants[id]) + '. Value of id is : ' + str(id) + '\n')
        del self.restaurants[id]

write_to_file('api-logs.txt','creating dictionary messag_fields\n')
"""
# message_fields dict is to be used with decorator function marshal_with while returning result of our methods like get, post etc.
# for eg: if our post method outputs 5 attributes but we wish to return only 2 attribute in REST RESPONSE then those 2 attributes
# should be added in the message_fields dict. Additionally the message_fields dict includes URI of the created resource in response.
"""
message_fields = {
    'id': fields.Integer, 
    'uri': fields.Url('message_endpoint'),
    'name': fields.String,
    'location': fields.String,
    'creation_date': fields.DateTime,
    'cuisine': fields.String,
    'contact': fields.String,
    'menu': fields.String
    #'photos':fields.List,
    #'average_cost':fields.Integer 
}
write_to_file('api-logs.txt','  dictionary message_fields created as : ' + str(message_fields) + '\n')
write_to_file('api-logs.txt','creating instance of ModelManager class named message_manager\n')
message_manager = ModelManager()
write_to_file('api-logs.txt','created instance message_manager as : ' + str(message_manager) + '\n')

# Below class provides a RESTful class for our resource which helps us to serve REST API requests like GET, PATCH etc on the resource.
class Restaurant(Resource):
    def abort_if_restaurant_doesnt_exist(self, id):
        write_to_file('api-logs.txt','inside Restaurant class abort_if_restaurant_doesnt_exist\n')
        write_to_file('api-logs.txt','  checking whether id exists for given id : ' + str(id) + '\n')
        if id not in message_manager.restaurants:
            abort(status.HTTP_404_NOT_FOUND, message="Restaurant {0} doesn't exist".format(id))

    @marshal_with(message_fields)
    def get(self, id):
        write_to_file('api-logs.txt','inside Restaurant class get()\n')
        write_to_file('api-logs.txt','  getting Restaurant for id : ' + str(id) + '\n')
        self.abort_if_restaurant_doesnt_exist(id) 
        return message_manager.get_restaurant(id)
        write_to_file('api-logs.txt','  got Restaurant for given id as : ' + str(message_manager.get_restaurant(id)) + '\n')

    def delete(self, id):
        write_to_file('api-logs.txt','inside Restaurant class delete()\n')
        write_to_file('api-logs.txt','  method input id as : ' + str(id) + '\n')
        self.abort_if_restaurant_doesnt_exist(id)
        message_manager.delete_restaurant(id)
        return '', status.HTTP_204_NO_CONTENT
        write_to_file('api-logs.txt','  method return : ' + str(('',status.HTTP_204_NO_CONTENT)) + '\n')
    @marshal_with(message_fields)
    def patch(self, id):
        write_to_file('api-logs.txt','inside Restaurant class patch()\n')
        self.abort_if_restaurant_doesnt_exist(id)
        restaurant = message_manager.get_restaurant(id) # message in an instance of RestaurantModel class that has the given id.
        parser = reqparse.RequestParser() # parser is used to read the arguments coming in the PATCH REQUEST
        parser.add_argument('name', type=str)
        parser.add_argument('location', type=str)
        parser.add_argument('cuisine', type=list,location='json')
        parser.add_argument('contact', type=list,location='json')
        parser.add_argument('menu', type=dict)
        #parser.add_argument('photos', type=list)
        #parser.add_argument('average_cost', type=int)
        args = parser.parse_args() # arguments in the PATCH REQUEST are saved in args dictionary
        write_to_file('api-logs.txt','  args recevied in PATCH request are : ' + str(args) + '\n')
        # below, the value of arguments received through PATCH REQUEST is applied to the message object with given id
        if 'name' in args and args['name']!=None:
            restaurant.name = args['name']
        if 'location' in args and args['location']!=None: 
            restaurant.location = args['location']
        if 'contact' in args and args['contact']!=None:
            restaurant.contact = args['contact']
        if 'menu' in args and args['menu']!=None:
            restaurant.menu = args['menu']
        #if 'photos' in args:
        #    restaurant.photos = args['photos']
        if 'cuisine' in args:
            restaurant.cuisine = args['cuisine']
        #if 'average_cost' in args:
        #    restaurant.average_cost = args['average_cost']
        write_to_file('api-logs.txt','  updated RestaurantModel object is : ' + str(restaurant) + '\n')
        return restaurant

# Below class provides a RESTful class for our resource which helps us to serve REST API requests like GET, PATCH etc on the resource.
class RestaurantList(Resource):
    @marshal_with(message_fields)
    # below get will be used to provide list of all restaurants.
    def get(self):
        write_to_file('api-logs.txt','inside RestaurantList class get()\n')
        write_to_file('api-logs.txt','  get list of restaurants : ' + str(message_manager.restaurants))
        return [v for v in message_manager.restaurants.values()]
 
    @marshal_with(message_fields) 
    def post(self): 
        write_to_file('api-logs.txt','inside RestaurantList class post()\n')
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name cannot be blank!') 
        parser.add_argument('location', type=str, required=True, help='Location cannot be blank!')
        parser.add_argument('cuisine', type=list, location='json',required=True, help='Cuisine category cannot be blank!')
        parser.add_argument('contact', type=list, location='json',required=True, help='Contact cannot be blank!')
        #parser.add_argument('photos', type=list, required=False, help='Photos are optional')
        #parser.add_argument('average_cost', type=int, required=False, help='Average cost is optional')
        parser.add_argument('menu', type=dict, required=False, help='Menu is optional')
        args = parser.parse_args()
        write_to_file('api-logs.txt','  arguments parsed in POST request are : ' + str(args) + '\n')

        #create a new RestaurantModel object with the arguments received in the POST request
        restaurant = RestaurantModel(
            name=args['name'], 
            location=args['location'], 
            creation_date=datetime.now(utc), 
            cuisine=args['cuisine'],
            contact=args['contact'],
            menu=args['menu'],
            #photos=args['photos'],
            #average_cost=args['average_cost']
            )

        write_to_file('api-logs.txt','  A RestaurantModel class object is created with args in POST REQ as : ' + str(restaurant) + '\n')
        message_manager.add_restaurant(restaurant)
        write_to_file('api-logs.txt','  POST method returns : ' + str(str(restaurant) + ' ' + str(status.HTTP_201_CREATED)) + '\n')
        write_to_file('api-logs.txt','  Data type for contact is : ' + str(type(restaurant.contact)) + '\n')
        write_to_file('api-logs.txt','  Data type for menu is : ' + str(type(restaurant.menu)) + '\n')
        write_to_file('api-logs.txt','  Data type for cuisine is : ' + str(type(restaurant.cuisine)) + '\n')
        return restaurant, status.HTTP_201_CREATED

"""
Configuring resource routing and endpoints:
The following lines create the main entry point for
the application, initialize it with a Flask 
application and configure the resource routing for 
the api
"""
app = Flask(__name__) 
api = Api(app) 
"""
Route a URL to the resource:
When there is a REST request to the API and the URL matches one of the URLs specified in the 
api.add_resource method, Flask will call the method that matches the HTTP verb in the 
request for the specified class.
"""
api.add_resource(RestaurantList, '/api/restaurants/')
api.add_resource(Restaurant, '/api/restaurants/<int:id>', endpoint='message_endpoint')

if __name__ == '__main__': 
    app.run(debug=True)
