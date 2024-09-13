from ..Utility.Common import *
from typing import List
class GrowthRate(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/growth-rate/" + str(id))
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"name",str)
    
    @property
    def formula(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"formula",str)
    
    @property
    def descriptions(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"descriptions",Description)
    
    @property
    def levels(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"levels",GrowthRateExperienceLevel)
    
    @property
    def pokemon_species(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"pokemon_species",NamedAPIResource)
    
    
class GrowthRateExperienceLevel:
    def __init__(self,json_data):
        self.__json_data = json_data
        

    @property
    def level(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"level",int)
    
    @property
    def experience(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"experience",int)
    