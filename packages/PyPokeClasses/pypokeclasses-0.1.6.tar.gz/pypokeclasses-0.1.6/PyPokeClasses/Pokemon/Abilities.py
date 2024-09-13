from ..Utility.Common import *
from typing import List
class Abilities(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/ability/" + str(id))
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"name",str)
    
    @property
    def is_main_series(self) -> Union[bool,None]:
        return Functions.convert_to_type(self._json_data,"is_main_series",bool)
    
    @property
    def generation(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"generation",NamedAPIResource)
    
    @property
    def names(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"names",Name)
    
    @property
    def effect_entries(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"effect_entries",VerboseEffect)
    
    @property
    def effect_changes(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"effect_changes",AbilityEffectChange)
    
    @property
    def flavor_text_entries(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"flavor_text_entries",AbilityFlavorText)
    
    @property
    def pokemon(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"pokemon",AbilityPokemon)
    
    
class AbilityEffectChange:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def effect_entries(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"effect_entries",Effect)

    @property
    def version_group(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"version_group",NamedAPIResource)
    
class AbilityFlavorText:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def flavor_text(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"flavor_text",str)
    
    @property
    def language(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"language",NamedAPIResource)
    
    @property
    def version_group(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"version_group",NamedAPIResource)
    
class AbilityPokemon:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def is_hidden(self) -> Union[bool,None]:
        return Functions.convert_to_type(self.__json_data,"is_hidden",bool)
    
    @property
    def slot(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"slot",int)
    
    @property
    def pokemon(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"pokemon",NamedAPIResource)