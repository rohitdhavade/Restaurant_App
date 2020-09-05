
import sys
sys.path.append("c:\\Users\\rdhavade\\OneDrive\\OneDrive - Cisco\\working_directory\\FoodApp\\FoodAPI")
sys.path.append("..")
from flask import Flask 
from flask_restful import abort, Api, fields, marshal_with, reqparse, Resource 
from datetime import datetime 
from models import UserModel 
import status 
from pytz import utc,timezone
import pytz
from  Login.login import LoginWithInMemoryDb
from modelmanager.usermodelmanager import ModelManager

def set_date():
    date = datetime.now()
    timezone = pytz.timezone("Asia/Kolkata")
    d_aware = timezone.localize(date)
    date_format = "%d-%b-%Y %H:%M:%S"
    return date,date_format

def write_to_file(file_name:str,content:str):
    with open(file_name,'a') as outfileh:
        current_date, date_format = set_date()
        outfileh.write(current_date.strftime(date_format) + ' ' + content)

write_to_file('user-api-logs.txt','started code\n')
write_to_file('user-api-logs.txt','creating dictionary message_fields\n')
"""
# message_fields dict is to be used with decorator function marshal_with while returning result of our methods like get, post etc.
# for eg: if our post method outputs 5 attributes but we wish to return only 2 attribute in REST RESPONSE then those 2 attributes
# should be added in the message_fields dict. Additionally the message_fields dict includes URI of the created resource in response.
"""
message_fields = {
    'id': fields.Integer, 
    'uri': fields.Url('user_endpoint'),
    'name': fields.String,
    'email_id': fields.String,
    'creation_date': fields.DateTime,
    'contact': fields.String,
    'username': fields.String,
    'user_type': fields.String
    #'photos':fields.List,
    #'average_cost':fields.Integer 
}
write_to_file('user-api-logs.txt','  dictionary message_fields created as : ' + str(message_fields) + '\n')
write_to_file('user-api-logs.txt','creating instance of ModelManager class named message_manager\n')
message_manager = ModelManager.get_instance()
write_to_file('user-api-logs.txt','created instance message_manager as : ' + str(message_manager) + '\n')

# Below class provides a RESTful class for our resource which helps us to serve REST API requests like GET, PATCH etc on the resource.
class User(Resource):
    def abort_if_user_doesnt_exist(self, id):
        write_to_file('user-api-logs.txt','inside User class abort_if_user_doesnt_exist\n')
        write_to_file('user-api-logs.txt','  checking whether user exists for given id : ' + str(id) + '\n')
        if id not in message_manager.users:
            abort(status.HTTP_404_NOT_FOUND, message="User with id {0} doesn't exist".format(id))

    @marshal_with(message_fields)
    def get(self, id):
        write_to_file('user-api-logs.txt','inside User class get()\n')
        write_to_file('user-api-logs.txt','  getting User for id : ' + str(id) + '\n')
        self.abort_if_user_doesnt_exist(id)
        return message_manager.get_user(id)
        write_to_file('user-api-logs.txt','  got User for given id as : ' + str(message_manager.get_user(id)) + '\n')

    def delete(self, id):
        write_to_file('user-api-logs.txt','inside User class delete()\n')
        write_to_file('user-api-logs.txt','  method input id as : ' + str(id) + '\n')
        self.abort_if_user_doesnt_exist(id)
        message_manager.delete_user(id)
        return '', status.HTTP_204_NO_CONTENT
        write_to_file('user-api-logs.txt','  method return : ' + str(('',status.HTTP_204_NO_CONTENT)) + '\n')
    @marshal_with(message_fields)
    def patch(self, id):
        write_to_file('user-api-logs.txt','inside User class patch()\n')
        self.abort_if_user_doesnt_exist(id)
        user = message_manager.get_user(id) # message in an instance of UserModel class that has the given id.
        parser = reqparse.RequestParser() # parser is used to read the arguments coming in the PATCH REQUEST
        parser.add_argument('name', type=str)
        parser.add_argument('email_id', type=str)
        parser.add_argument('contact', type=str)
        parser.add_argument('password', type=str)
        #parser.add_argument('average_cost', type=int)
        args = parser.parse_args() # arguments in the PATCH REQUEST are saved in args dictionary
        write_to_file('user-api-logs.txt','  args recevied in PATCH request are : ' + str(args) + '\n')
        # below, the value of arguments received through PATCH REQUEST is applied to the message object with given id
        if 'name' in args and args['name']!=None:
            user.name = args['name']
        if 'email_id' in args and args['email_id']!=None: 
            user.email_id = args['email_id']
        if 'contact' in args and args['contact']!=None:
            user.contact = args['contact']
        if 'password' in args and args['password']!=None:
            user.password = args['password']

        write_to_file('user-api-logs.txt','  updated UserModel object is : ' + str(user) + '\n')
        return user

# Below class provides a RESTful class for our resource which helps us to serve REST API requests like GET, PATCH etc on the resource.
class UserList(Resource):
    @marshal_with(message_fields)
    # below get will be used to provide list of all users.
    def get(self):
        write_to_file('user-api-logs.txt','inside UserList class get()\n')
        write_to_file('user-api-logs.txt','  get list of users : ' + str(message_manager.users))
        return [v for v in message_manager.users.values()]
 
    @marshal_with(message_fields) 
    def post(self):
        write_to_file('user-api-logs.txt','inside UserList class post()\n')
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name cannot be blank!') 
        parser.add_argument('email_id', type=str, required=True, help='Email-id cannot be blank!')
        parser.add_argument('contact', type=str, required=False, help='Provide your mobile number.')
        parser.add_argument('username', type=str, required=True, help='Username cannot be blank!')
        parser.add_argument('password', type=str, required=True, help='Please provide password.')
        #parser.add_argument('average_cost', type=int, required=False, help='Average cost is optional')
        parser.add_argument('user_type', type=str, required=True, help='user_type is required.')
        args = parser.parse_args()
        write_to_file('user-api-logs.txt','  arguments parsed in POST request are : ' + str(args) + '\n')

        #create a new UserModel object with the arguments received in the POST request
        current_date, date_format = set_date()
        current_date_in_str = current_date.strftime(date_format)
        user = UserModel(
            name=args['name'], 
            email_id=args['email_id'], 
            creation_date=current_date.strptime(current_date_in_str,date_format),
            username=args['username'],
            password=args['password'],
            user_type=args['user_type'],
            #photos=args['photos'],
            #average_cost=args['average_cost']
            )

        write_to_file('user-api-logs.txt','  A UserModel class object is created with args in POST REQ as : ' + str(user) + '\n')
        message_manager.add_user(user)
        write_to_file('user-api-logs.txt','  POST method returns : ' + str(str(user) + ' ' + str(status.HTTP_201_CREATED)) + '\n')
        return user, status.HTTP_201_CREATED

check_username_fields = {
    "username" : fields.String,
    "username_exists" : fields.Boolean
}
class check_username(Resource):
    @marshal_with(check_username_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='username is required.')
        args = parser.parse_args()
        username = args['username']
        username_exists = message_manager.check_username(username)
        return_dict = {'username':username,'username_exists':username_exists}
        return return_dict
class validate_username(Resource):
    def post(self):
        write_to_file('user-api-logs.txt','INSIDE CLASS validate_username method get()\n')
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='username is required.')
        parser.add_argument('password', type=str, required=True, help='password is required.')
        args = parser.parse_args()
        write_to_file('user-api-logs.txt','  value of args parsed from GET REQ are :' + str(args) + '\n')
        login_object = LoginWithInMemoryDb(
            username = args['username'],
            password = args['password']
        )
        result = login_object.validate_username()
        write_to_file('user-api-logs.txt','  result obtained from validate_username as: ' + str(result) + '\n')
        return result
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
api.add_resource(UserList, '/api/users/')
api.add_resource(User, '/api/users/<int:id>', endpoint='message_endpoint')
api.add_resource(check_username,'/api/users/check_username')
api.add_resource(validate_username,'/api/users/validate_username')
if __name__ == '__main__': 
    app.run(debug=True)
