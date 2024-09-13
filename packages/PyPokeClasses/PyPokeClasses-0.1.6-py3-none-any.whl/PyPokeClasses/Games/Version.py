from ..Utility.Common import *
from typing import List

class Version(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/version/" + str(id))
        
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
    def version_group(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"version_group",NamedAPIResource)
    
    