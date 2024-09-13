from ..Utility.Common import *
from typing import List

class Language(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/language/" + str(id))
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"name",str)
    
    @property
    def official(self) -> Union[bool,None]:
        return Functions.convert_to_type(self._json_data,"official",bool)
    
    @property
    def iso639(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"iso639",str)
    
    @property
    def iso3166(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"iso3166",str)
    
    @property
    def names(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"names",Name)
