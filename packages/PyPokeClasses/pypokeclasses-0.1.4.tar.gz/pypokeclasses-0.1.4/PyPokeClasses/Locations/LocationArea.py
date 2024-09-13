from ..Utility.Common import *
from typing import List

class LocationArea(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/location-area/" + str(id))
        
        
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
    def encounter_method_rates(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"encounter_method_rates",EncounterMethodRate)

    @property
    def location(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"location",NamedAPIResource)
    
    
    @property
    def names(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"names",Name)
    
    @property
    def pokemon_encounters(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"pokemon_encounters",PokemonEncounter)

class EncounterMethodRate:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def encounter_method(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"encounter_method",NamedAPIResource)
    
    @property
    def version_details(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"version_details",EncounterVersionDetails)
    
class EncounterVersionDetails:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def rate(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"rate",int)
    
    @property
    def version(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"version",NamedAPIResource)
    
class PokemonEncounter:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def pokemon(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"pokemon",NamedAPIResource)
    
    @property
    def version_details(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"version_details",VersionEncounterDetail)
    
