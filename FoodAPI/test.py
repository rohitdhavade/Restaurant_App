
from abc import ABC
class person(ABC):
    def __init__(self,name:str):
        self.name = name

class student(person):
    pass

class extc(student):
    naukri = "nahi"
