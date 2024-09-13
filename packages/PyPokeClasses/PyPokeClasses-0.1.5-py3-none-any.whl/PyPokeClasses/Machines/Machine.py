from ..Utility.Common import *
from typing import List

class Machine(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/machine/" + str(id))
        
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def item(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"item",NamedAPIResource)
  
    @property
    def move(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"move",NamedAPIResource)
    
    @property
    def version_group(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"version_group",NamedAPIResource)