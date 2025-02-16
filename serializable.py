from abc import ABC, abstractmethod
from tinydb import Query, TinyDB
from typing import Self

class Serializable(ABC):
    db_connector: TinyDB = None

    def __init__(self, id) -> None:
        self.id = id

    @classmethod
    @abstractmethod
    def instantiate_from_dict(cls, data: dict) -> Self:
        pass

    def store_data(self):
        print("Storing data...")

        query = Query()
        # upsert: https://tinydb.readthedocs.io/en/latest/usage.html#upserting-data
        result = self.db_connector.upsert(self.__to_dict(), query.id == self.id)
        if result:
            print("Data updated.")
        else:
            print("Data inserted.")

    
    def delete(self):
        print("Deleting data...")
        query = Query()
        if self.db_connector.remove(query.id == self.id):
            print("Data deleted.")
        else:
            print("Data not found.")
    
    @classmethod
    def find_by_attribute(cls, by_attribute: str, attribute_value: str, num_to_return=1) -> Self | list[Self]:
        if cls.db_connector is None:
            raise ValueError("db_connector wurde nicht initialisiert!")
        
        DeviceQuery = Query()
        result = cls.db_connector.search(DeviceQuery[by_attribute] == attribute_value)

        if result:
            if num_to_return == -1:
                num_to_return = len(result)

            data = result[:num_to_return]
            point_results = [cls.instantiate_from_dict(d) for d in data]
            return point_results if num_to_return > 1 else point_results[0]
        else:
            return None

           
    @classmethod
    def find_all(cls) -> list[Self]:
        mech = []
        for mech_data in cls.db_connector.all():
            mech.append(cls.instantiate_from_dict(mech_data))
        return mech

    def __repr__(self):
        return self.__str__()
    
    @abstractmethod
    def __str__(self):
        pass
    

    def __to_dict(self, *args):
        """
        This function converts an object recursively into a dict.
        It is not necessary to understand how this function works!
        For the sake of simplicity it doesn't handle class attributes and callable objects like (callback) functions as attributes well
        """

        #If no object is passed to the function convert the object itself
        if len(args) > 0:
            obj = args[0] #ignore all other objects but the first one
        else:
            obj = self

        if isinstance(obj, dict):
            #If the object is a dict try converting all its values into dicts also
            data = {}
            for (k, v) in obj.items():
                data[k] = self.__to_dict(v)
            return data
        elif hasattr(obj, "__iter__") and not isinstance(obj, str):
            #If the object is iterable (lists, etc.) try converting all its values into dicts
            #Strings are also iterable, but theses should not be converted
            data = [self.__to_dict(v) for v in obj]
            return data
        elif hasattr(obj, "__dict__"):
            #If its an object that has a __dict__ attribute this can be used
            data = []
            for k, v in obj.__dict__.items():
                #Iterate through all items of the __dict__ and and try converting each value to a dict
                #The resulting key value pairs are stored as tuples in a list that is then converted to a final dict
                data.append((k, self.__to_dict(v)))
            return dict(data)
        else:
            return obj