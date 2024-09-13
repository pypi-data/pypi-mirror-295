from ..Utility.Common import *
from typing import List

class VersionGroup(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/version-group/" + str(id))
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"name",str)
    
    
    @property
    def order(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"order",int)
    
    @property
    def generation(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"generation",NamedAPIResource)
    
    @property
    def move_learn_methods(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"move_learn_methods",NamedAPIResource)
    
    @property
    def pokedexes(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"pokedexes",NamedAPIResource)

    @property
    def regions(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"regions",NamedAPIResource)
    
    @property
    def versions(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"versions",NamedAPIResource)
    