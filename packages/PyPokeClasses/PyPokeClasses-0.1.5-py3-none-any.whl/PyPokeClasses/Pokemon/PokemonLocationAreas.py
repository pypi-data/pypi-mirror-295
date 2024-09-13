from ..Utility.Common import *
from typing import List
class PokemonLocationAreas(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/pokemon/" + str(id) + "/encounters")
        
    @property
    def location_area(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"location_area",NamedAPIResource)
    
    
    @property
    def version_details(self) -> Union[List,None]:
        return Functions.convert_to_type(self._json_data,"version_details",VersionEncounterDetail)
    