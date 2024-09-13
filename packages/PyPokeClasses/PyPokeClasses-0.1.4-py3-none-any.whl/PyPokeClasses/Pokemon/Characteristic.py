from ..Utility.Common import *
from typing import List
class Characteristic(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/characteristic/" + str(id))
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def gene_modulo(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"gene_modulo",int)

    @property
    def possible_values(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"possible_values",int)  
    
    @property
    def highest_stat(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"highest_stat",NamedAPIResource)
    
    @property
    def descriptions(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"descriptions",Description)  