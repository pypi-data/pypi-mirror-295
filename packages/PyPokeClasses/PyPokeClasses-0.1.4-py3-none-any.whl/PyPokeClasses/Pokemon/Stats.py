from ..Utility.Common import *
from typing import List
class MoveStatAffectSets:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def increase(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"increase",MoveStatAffect)
    
    @property
    def decrease(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"decrease",MoveStatAffect)
      
class MoveStatAffect:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def change(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"change",int)
    
    @property
    def move(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"move",NamedAPIResource)
    
    
class NatureStatAffectSets:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def increase(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"increase",NamedAPIResource)
    
    @property
    def decrease(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"decrease",NamedAPIResource)

class Stats(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/stat/" + str(id))
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"name",str)
    
    @property
    def game_index(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"game_index",int)
    
    @property
    def is_battle_only(self) -> Union[bool,None]:
        return Functions.convert_to_type(self._json_data,"is_battle_only",bool)
    
    @property
    def affecting_moves(self) -> Union[MoveStatAffectSets,None]:
        return Functions.convert_to_type(self._json_data,"affecting_moves",MoveStatAffectSets)
    
    @property
    def affecting_natures(self) -> Union[NatureStatAffectSets,None]:
        return Functions.convert_to_type(self._json_data,"affecting_natures",NatureStatAffectSets)
    
    @property
    def characteristics(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"characteristics",APIResource)
    
    @property
    def move_damage_class(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"move_damage_class",NamedAPIResource)
    
    @property
    def names(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"names",Name)

