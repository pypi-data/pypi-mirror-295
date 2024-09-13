from ..Utility.Common import *
from typing import List
class PokemonShapes(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/pokemon-shape/" + str(id))
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"name",str)
    
    @property
    def awesome_names(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"awesome_names",AwesomeName)
    
    @property
    def names(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"names",Name)
    
    @property
    def pokemon_species(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"pokemon_species",NamedAPIResource)
    
class AwesomeName:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def awesome_name(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"awesome_name",str)
    
    @property
    def language(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"language",NamedAPIResource)
    
