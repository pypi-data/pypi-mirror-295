from ..Utility.Common import *
from typing import List

class Generation(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/generation/" + str(id))
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"name",str)
    
    @property
    def abilities(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"abilities",NamedAPIResource)
    
    @property
    def names(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"names",Name)
    
    @property
    def main_region(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"main_region",NamedAPIResource)
    
    @property
    def moves(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"moves",NamedAPIResource)

    @property
    def pokemon_species(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"pokemon_species",NamedAPIResource)
    
    @property
    def types(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"types",NamedAPIResource)
    
    @property
    def version_groups(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"version_groups",NamedAPIResource)