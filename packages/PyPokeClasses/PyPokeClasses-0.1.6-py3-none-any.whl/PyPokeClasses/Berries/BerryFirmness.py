from ..Utility.Common import *
from typing import List

class BerryFirmness(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/berry-firmness/" + str(id))
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"name",str)

    @property
    def berries(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"berries",NamedAPIResource)
    
    @property
    def names(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"names",Name)
    