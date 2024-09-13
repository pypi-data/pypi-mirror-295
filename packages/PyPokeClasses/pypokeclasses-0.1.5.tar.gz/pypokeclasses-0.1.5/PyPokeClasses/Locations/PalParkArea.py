from ..Utility.Common import *
from typing import List

class PalParkArea(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/pal-park-area/" + str(id))
        
        
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
    def pokemon_encounters(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"pokemon_encounters",PalParkEncounterSpecies)
    

class PalParkEncounterSpecies:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def base_score(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"base_score",int)

    @property
    def rate(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"rate",int)
    
    @property
    def pokemon_species(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"pokemon_species",NamedAPIResource)
    