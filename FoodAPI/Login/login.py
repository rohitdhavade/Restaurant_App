import sys
sys.path.append("c:\\Users\\rdhavade\\OneDrive\\OneDrive - Cisco\\working_directory\\FoodApp\\FoodAPI")
sys.path.append("..")
from abc import ABC, abstractmethod
from modelmanager.usermodelmanager import ModelManager
from datetime import datetime 
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
filename = 'login.py_logs.txt'

# Provide an interface for login methods which can be implemented in concrete classes
class LoginInterface(ABC):
    def __init__(self,username:str,password:str):
        write_to_file(filename,'INSIDE CLASS LoginInterface constructor __init__\n')
        self.username = username
        self.password = password
        write_to_file(filename,'  instance created as username:password - ' + str(self.username) + ':' + str(self.password) + '\n')
    @abstractmethod
    def validate_username(self):
        pass

# below is implemention of Login interface which uses in memory database for username authentication
class LoginWithInMemoryDb(LoginInterface):
    write_to_file(filename, 'INSIDE CLASS LoginWithInMemoryDb\n')
    model_manager_object = ModelManager.get_instance()
    users_dict = model_manager_object.users
    write_to_file(filename,'  obtained users_dict as : ' + str(users_dict) + '\n')
    result:dict = {'Authentication_Status:' : 'Authentication_Failed'} # by default we assume authentication fails
    def validate_username(self)  -> {'Authentication_Status':'Success or Failed'}:
        for id in self.users_dict:
            user_object = self.users_dict[id]
            if user_object.username == self.username:
                if user_object.password == self.password:
                    self.result = {'Authentication_Status:' : 'Authentication_Success'}
                    return self.result
                else:
                    return self.result
        self.result = {'Authentication_Status:' : 'Username_Does_Not_Exist'}
        return self.result
