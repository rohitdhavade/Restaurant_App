from flask import Flask 
from flask_restful import abort, Api, fields, marshal_with, reqparse, Resource 
from datetime import datetime 
from models import MessageModel 
import status 
from pytz import utc 

def write_to_file(file_name:str,content:str):
    with open(file_name,'a') as outfileh:
        outfileh.write(content)

write_to_file('api-logs.txt','started code\n')

class MessageManager(): 
    last_id = 0 
    def __init__(self): 
        write_to_file('api-logs.txt','inside class MessageManager __init__\n')
        self.messages = {} # dictionary of MessageModel class instances
        write_to_file('api-logs.txt','  value of messages dict is : ' + str(self.messages))
    def insert_message(self, message):
        write_to_file('api-logs.txt','inside class MessageManager insert_message()\n')
        self.__class__.last_id += 1 
        message.id = self.__class__.last_id 
        write_to_file('api-logs.txt','  value of message.id is : ' + str(message.id) + '\n')
        write_to_file('api-logs.txt','  value of message is : ' + str(message)+ '\n')
        self.messages[self.__class__.last_id] = message 
 
    def get_message(self, id): 
        write_to_file('api-logs.txt','inside class MessageManager get_message()\n')
        write_to_file('api-logs.txt','  value of id is : ' + str(id) + '\n')
        return self.messages[id] # returns an instance of MessageModel class with given id
 
    def delete_message(self, id): 
        write_to_file('api-logs.txt','inside class MessageManager delete_message\n')
        write_to_file('api-logs.txt','  value of message is : ' + str(self.messages[id]) + '. Value of id is : ' + str(id) + '\n')
        del self.messages[id] 

write_to_file('api-logs.txt','creating dictionary messag_fields\n')
message_fields = { 
    'id': fields.Integer, 
    'uri': fields.Url('message_endpoint'), 
    'message': fields.String, 
    'duration': fields.Integer, 
    'creation_date': fields.DateTime, 
    'message_category': fields.String, 
    'printed_times': fields.Integer, 
    'printed_once': fields.Boolean 
}
write_to_file('api-logs.txt','  dictionary message_fields created as : ' + str(message_fields) + '\n')
write_to_file('api-logs.txt','creating instance of MessageManager class named message_manager\n')
message_manager = MessageManager()
write_to_file('api-logs.txt','created instance message_manager as : ' + str(message_manager) + '\n')

class Message(Resource):
    def abort_if_message_doesnt_exist(self, id):
        write_to_file('api-logs.txt','inside Message class abort_if_message_doesnt_exist\n')
        write_to_file('api-logs.txt','  checking whether id exists for given id : ' + str(id) + '\n')
        if id not in message_manager.messages: 
            abort(status.HTTP_404_NOT_FOUND, message="Message {0} doesn't exist".format(id))

    @marshal_with(message_fields) 
    def get(self, id):
        write_to_file('api-logs.txt','inside Message class get()\n')
        write_to_file('api-logs.txt','  getting message for id : ' + str(id) + '\n')
        self.abort_if_message_doesnt_exist(id) 
        return message_manager.get_message(id)
        write_to_file('api-logs.txt','  got message for given id as : ' + str(message_manager.get_message(id)) + '\n')

    def delete(self, id): 
        write_to_file('api-logs.txt','inside Message class delete()\n')
        write_to_file('api-logs.txt','  method input id as : ' + str(id) + '\n')
        self.abort_if_message_doesnt_exist(id) 
        message_manager.delete_message(id) 
        return '', status.HTTP_204_NO_CONTENT 
        write_to_file('api-logs.txt','  method return : ' + str(('',status.HTTP_204_NO_CONTENT)) + '\n')
    @marshal_with(message_fields) 
    def patch(self, id): 
        write_to_file('api-logs.txt','inside Message class patch()\n')
        self.abort_if_message_doesnt_exist(id) 
        message = message_manager.get_message(id) # message in an instance of MessageModel class that has the given id.
        parser = reqparse.RequestParser() # parser is used to read the arguments in the PATCH REQUEST
        parser.add_argument('message', type=str) 
        parser.add_argument('duration', type=int) 
        parser.add_argument('printed_times', type=int) 
        parser.add_argument('printed_once', type=bool) 
        args = parser.parse_args() # arguments in the PATCH REQUEST are saved in args dictionary
        write_to_file('api-logs.txt','  args recevied in PATH request are : ' + str(args) + '\n')
        # below, the value of arguments received through PATH REQUEST is applied to the message object with given id
        if 'message' in args: 
            message.message = args['message'] 
        if 'duration' in args: 
            message.duration = args['duration'] 
        if 'printed_times' in args: 
            message.printed_times = args['printed_times'] 
        if 'printed_once' in args: 
            message.printed_once = args['printed_once'] 
        write_to_file('api-logs.txt','  updated MessageModel object is :' + str(message) + '\n')
        return message 

class MessageList(Resource): 
    @marshal_with(message_fields) 
    def get(self): 
        write_to_file('api-logs.txt','inside MessageList class get()\n')
        write_to_file('api-logs.txt','  get list of messages : ' + str(message_manager.messages))
        return [v for v in message_manager.messages.values()] 
 
    @marshal_with(message_fields) 
    def post(self): 
        write_to_file('api-logs.txt','inside MessageList class post()\n')
        parser = reqparse.RequestParser() 
        parser.add_argument('message', type=str, required=True, help='Message cannot be blank!') 
        parser.add_argument('duration', type=int, required=True, help='Duration cannot be blank!') 
        parser.add_argument('message_category', type=str, required=True, help='Message category cannot be blank!') 
        args = parser.parse_args() 
        write_to_file('api-logs.txt','  arguments parse in POST request are : ' + str(args) + '\n')
        message = MessageModel( 
            message=args['message'], 
            duration=args['duration'], 
            creation_date=datetime.now(utc), 
            message_category=args['message_category'] 
            )
        write_to_file('api-logs.txt','  A MessageModel class object is created with args in POST REQ as : ' + str(message) + '\n')
        message_manager.insert_message(message)  
        write_to_file('api-logs.txt','  POST method returns : ' + str((message, status.HTTP_201_CREATED)) + '\n')
        return message, status.HTTP_201_CREATED

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
When there is a request to the API and the URL 
matches one of the URLs specified in the 
api.add_resource method, Flask will call the method 
that matches the HTTP verb in the request for the 
specified class.
"""
api.add_resource(MessageList, '/api/messages/')
api.add_resource(Message, '/api/messages/<int:id>', endpoint='message_endpoint')

if __name__ == '__main__': 
    app.run(debug=True)
