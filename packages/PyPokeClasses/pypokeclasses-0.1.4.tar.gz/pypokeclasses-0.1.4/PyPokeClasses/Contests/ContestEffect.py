from ..Utility.Common import *
from typing import List

class ContestEffect(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/contest-effect/" + str(id))
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def appeal(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"appeal",int)
    
    @property
    def jam(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"jam",int)
    
    @property
    def effect_entries(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"effect_entries",Effect)
    
    @property
    def flavor_text_entries(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"flavor_text_entries",FlavorText)
