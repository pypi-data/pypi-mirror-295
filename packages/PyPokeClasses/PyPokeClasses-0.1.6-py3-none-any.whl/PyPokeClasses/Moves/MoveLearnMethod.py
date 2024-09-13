from ..Utility.Common import *
from typing import List

class MoveLearnMethod(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/move-damage-class/" + str(id))
        
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"name",str)
    
    @property
    def descriptions(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"descriptions",Description)
    
    @property
    def names(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"names",Name)
    
    @property
    def version_groups(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"version_groups",NamedAPIResource)