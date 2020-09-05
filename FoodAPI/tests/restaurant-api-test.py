import sys
sys.path.append('.')
sys.path.append('..')
sys.path.append("c:\\Users\\rdhavade\\OneDrive\\OneDrive - Cisco\\working_directory\\FoodApp\\FoodAPI")
from models import RestaurantModel
from api import ModelManager
from pytz import utc,timezone
import pytz
from datetime import datetime 

def set_date():
    date = datetime.now()
    timezone = pytz.timezone("Asia/Kolkata")
    d_aware = timezone.localize(date)
    date_format = "%d-%b-%Y %H:%M:%S"
    return date,date_format

def write_to_file(file_name:str,content:str):
    with open(file_name,'a') as outfileh:
        current_date, date_format = set_date()
        outfileh.write(current_date.strftime(date_format) + ' ' + content + '\n')
filename = 'test-results.txt'
class ModelManagerTest(object):
    def __init__(self,restaurant_object):
        self.restaurant_object = restaurant_object
        self.modelmanager_instance = ModelManager()
    def test_add_restaurant(self):
        self.modelmanager_instance.add_restaurant(self.restaurant_object)
        assert len(self.modelmanager_instance.restaurants) != 0, write_to_file(filename,
        'FAILED:Test to add restaurant failed. Check api.py.ModelManager.add_restaurant().')
        for id in self.modelmanager_instance.restaurants:
            temp_result = 'Fail'
            restaurant_object = self.modelmanager_instance.restaurants[id]
            if restaurant_object.name == 'Royal Foods':
                write_to_file(filename,'SUCCESS:Test to add restaurant succeeded.api.py.ModelManager.add_restaurant()')
                temp_result = 'Pass'
                return id
                break
        if temp_result == 'Fail':
            write_to_file(filename,'FAILED:Test to add restaurant failed. Check api.py.ModelManager.add_restaurant()')
    def test_get_restaurant(self,id):
        res_obj = self.modelmanager_instance.get_restaurant(id)
        assert isinstance(res_obj,RestaurantModel), write_to_file(filename,
        'FAILED:Test to get restaurant failed. Restaurant Object is not instance of api.py.ModelManager')
        if res_obj.name == 'Royal Foods':
            write_to_file(filename,'SUCCESS: Test to get restaurant succeeded.api.py.ModelManager.get_restaurant()')

if __name__=='__main__':
    current_date, date_format = set_date()
    restaurant_model_object = RestaurantModel(name='Royal Foods',location='Sector-8, Nerul',cuisine=['North Indian','Chinese'],
        contact=['9232923200','8600049998'],menu={'Fried Rice':'INR.150','Chicken65':'INR.200','Chicken Tandoori':'INR.300'},
        creation_date=current_date)
    mmt = ModelManagerTest(restaurant_model_object)
    res_id = mmt.test_add_restaurant()
    mmt.test_get_restaurant(res_id)
