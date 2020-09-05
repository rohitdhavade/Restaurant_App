import sys
sys.path.append("c:\\Users\\rdhavade\\OneDrive\\OneDrive - Cisco\\working_directory\\FoodApp\\FoodAPI")
sys.path.append("..")
from datetime import datetime 
from models import UserModel 
import status 
from pytz import utc,timezone
import pytz

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

# Below class ModelManager is used to manage our resource with add, get, delete methods.
# these methods may operate with the database like, SQL to perform the required actions i.e. add, get, delete etc.
class ModelManager():
    last_id = 0
    __instance = None
    @staticmethod
    def get_instance():
        if ModelManager.__instance is None:
            ModelManager()
        return ModelManager.__instance
    def __init__(self):
        # we will implement singleton design pattern for this class since we should not create new instance otherwise
        # it will create a new empty users dict.
        write_to_file('user-api-logs.txt','inside class ModelManager __init__\n')
        if ModelManager.__instance is not None:
            raise Exception("Instance of ModelManager already exists!")
        else:
            self.users = {} # dictionary of UserModel class instances with key as id
            ModelManager.__instance = self
        write_to_file('user-api-logs.txt','  value of users dict is : ' + str(self.users))
    def add_user(self, user:UserModel):
        write_to_file('user-api-logs.txt','inside class ModelManager add_user()\n')
        self.__class__.last_id += 1
        user.id = self.__class__.last_id
        write_to_file('user-api-logs.txt','  value of user.id is : ' + str(user.id) + '\n')
        write_to_file('user-api-logs.txt','  value of user is : ' + str(user)+ '\n')
        self.users[self.__class__.last_id] = user
    def get_user(self, id):
        write_to_file('user-api-logs.txt','inside class ModelManager get_user()\n')
        write_to_file('user-api-logs.txt','  value of id is : ' + str(id) + '\n')
        return self.users[id] # returns an instance of UserModel class with given id
    def delete_user(self, id): 
        write_to_file('user-api-logs.txt','inside class ModelManager delete_user\n')
        write_to_file('user-api-logs.txt','  value of message is : ' + str(self.users[id]) + '. Value of id is : ' + str(id) + '\n')
        del self.users[id]
    def check_username(self,username):
        write_to_file('user-api-logs.txt','inside class ModelManager check_username()')
        for id in self.users:
            get_user_object = self.users[id]
            if get_user_object.username == username:
                return True
        return False
