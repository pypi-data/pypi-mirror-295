from ..Utility.Common import *
from typing import List

class BerryFlavor(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/berry-flavor/" + str(id))
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"name",str)

    @property
    def berries(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"berries",FlavorBerryMap)
    
    @property
    def contest_type(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"contest_type",NamedAPIResource)

    @property
    def names(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"names",Name)
    
class FlavorBerryMap:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def potency(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"potency",int)
    
    @property
    def berry(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"berry",NamedAPIResource)
    