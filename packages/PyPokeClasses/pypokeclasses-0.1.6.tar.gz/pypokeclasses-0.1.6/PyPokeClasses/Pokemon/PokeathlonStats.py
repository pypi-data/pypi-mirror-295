from ..Utility.Common import *
from typing import List

class NaturePokeathlonStatAffectSets:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def increase(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"increase",NaturePokeathlonStatAffect)
    
    @property
    def decrease(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"decrease",NaturePokeathlonStatAffect)
      
class NaturePokeathlonStatAffect:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def max_change(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"max_change",int)
    
    @property
    def nature(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"nature",NamedAPIResource)
    
class PokeathlonStats(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/pokeathlon-stat/" + str(id))
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"name",str)
    
    @property
    def names(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"names",Name)
    
    @property
    def affecting_natures(self) -> Union[NaturePokeathlonStatAffectSets,None]:
        return Functions.convert_to_type(self._json_data,"affecting_natures",NaturePokeathlonStatAffectSets)

 
    