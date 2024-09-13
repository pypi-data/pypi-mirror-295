from ..Utility.Common import *
from typing import List
class Natures(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/nature/" + str(id))
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"name",str)
    
    @property
    def decreased_stat(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"decreased_stat",NamedAPIResource)
    
    @property
    def increased_stat(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"increased_stat",NamedAPIResource)

    @property
    def hates_flavor(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"hates_flavor",NamedAPIResource)

    @property
    def likes_flavor(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"likes_flavor",NamedAPIResource)
    
    @property
    def pokeathlon_stat_changes(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"pokeathlon_stat_changes",NatureStatChange)
    
    @property
    def move_battle_style_preferences(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"move_battle_style_preferences",MoveBattleStylePreference)
    
    @property
    def names(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"names",Name)
    
class NatureStatChange:
    def __init__(self,json_data):
        self.__json_data = json_data
        

    @property
    def max_change(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"max_change",int)
    
    @property
    def pokeathlon_stat(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"pokeathlon_stat",NamedAPIResource)
    
class MoveBattleStylePreference:
    def __init__(self,json_data):
        self.__json_data = json_data
        

    @property
    def low_hp_preference(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"low_hp_preference",int)
    
    @property
    def high_hp_preference(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"high_hp_preference",int)
    
    @property
    def move_battle_style(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"move_battle_style",NamedAPIResource)