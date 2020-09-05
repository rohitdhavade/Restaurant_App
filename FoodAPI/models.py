from datetime import datetime
class RestaurantModel:
    def __init__(self, name:str, location:str, creation_date:datetime, cuisine:list, contact:list, menu:dict): # photos:list, average_cost:int):
        # We will automatically generate the new id
        self.id:int = 0 
        self.name = name 
        self.location = location 
        self.creation_date = creation_date 
        self.cuisine = cuisine 
        self.contact = contact
        self.menu = menu
        #self.photos = photos
        #self.average_cost = average_cost

    def __repr__(self):
        return str(self.__dict__)
    def __str__(self):
        return str(self.__dict__)

class UserModel:
    def __init__(self, name:str, email_id:str, username:str,password:str, user_type:str, creation_date:datetime):
        self.id:int = 0
        self.name = name
        self.email_id = email_id
        self.contact = 0
        self.username = username
        self.password = password
        self.creation_date = creation_date
        self.user_type = user_type # admin, or normal_user or restaurant_admin
        # admin user has rights to add, delete any restaurant.
        # normal_user has rights to only view all restaurants.
        # restaurant_admin user has rights to edit specific restaurant.
    def __repr__(self):
        return str(self.__dict__)
    def __str__(self):
        return str(self.__dict__)
