from ..Utility.Common import *
from typing import List

class Region(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/region/" + str(id))
        
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def locations(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"locations",NamedAPIResource)
    
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"name",str)
    
    @property
    def names(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"names",Name)

    @property
    def main_generation(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"main_generation",NamedAPIResource)

    @property
    def pokedexes(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"pokedexes",NamedAPIResource)
    
    @property
    def version_groups(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"version_groups",NamedAPIResource)
    