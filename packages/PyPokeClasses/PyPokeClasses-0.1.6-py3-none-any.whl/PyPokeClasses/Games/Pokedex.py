from ..Utility.Common import *
from typing import List

class Pokedex(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/pokedex/" + str(id))
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"name",str)
    
    @property
    def is_main_series(self) -> Union[bool,None]:
        return Functions.convert_to_type(self._json_data,"is_main_series",bool)
    
    @property
    def descriptions(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"descriptions",Description)
    
    @property
    def names(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"names",Name)
    
    @property
    def pokemon_entries(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"pokemon_entries",PokemonEntry)
    
    @property
    def region(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"region",NamedAPIResource)
    
    @property
    def version_groups(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"version_groups",NamedAPIResource)
    
    
    
class PokemonEntry:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def entry_number(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"entry_number",int)
    
    @property
    def pokemon_species(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"pokemon_species",NamedAPIResource)
    