from ..Utility.Common import *
from typing import List

class SuperContestEffect(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/super-contest-effect/" + str(id))
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def appeal(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"appeal",int)
    
    @property
    def flavor_text_entries(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"flavor_text_entries",FlavorText)
    
    @property
    def moves(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"moves",NamedAPIResource)
