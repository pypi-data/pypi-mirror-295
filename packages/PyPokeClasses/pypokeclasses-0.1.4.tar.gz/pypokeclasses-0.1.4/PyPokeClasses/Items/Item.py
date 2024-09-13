from ..Utility.Common import *
from typing import List

class ItemSprites:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"default",str)
    
class ItemHolderPokemon:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def pokemon(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"pokemon",NamedAPIResource)
    
    @property
    def version_details(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"version_details",ItemHolderPokemonVersionDetail)
    
class ItemHolderPokemonVersionDetail:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def rarity(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"rarity",int)
    
    @property
    def version(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"version",NamedAPIResource)

class Item(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/item/" + str(id))
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"name",str)
    
    @property
    def cost(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"cost",int)
    
    @property
    def fling_power(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"fling_power",int)
    
    @property
    def fling_effect(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"fling_effect",NamedAPIResource)
    
    @property
    def attributes(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"attributes",NamedAPIResource)
    
    @property
    def category(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"category",NamedAPIResource)
    
    @property
    def effect_entries(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"effect_entries",VerboseEffect)
    
    @property
    def flavor_text_entries(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"flavor_text_entries",VersionGroupFlavorText)

    @property
    def game_indices(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"game_indices",GenerationGameIndex)
    
    @property
    def names(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"names",Name)
    
    @property
    def sprites(self) -> Union[ItemSprites,None]:
        return Functions.convert_to_type(self._json_data,"sprites",ItemSprites)
    
    @property
    def held_by_pokemon(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"held_by_pokemon",ItemHolderPokemon)
    
    @property
    def baby_trigger_for(self) -> Union[APIResource,None]:
        return Functions.convert_to_type(self._json_data,"baby_trigger_for",APIResource)
    
    @property
    def machines(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"machines",MachineVersionDetail)
     

    