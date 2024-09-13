from ..Utility.Common import *
from typing import List

class ChainLink:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def is_baby(self) -> Union[bool,None]:
        return Functions.convert_to_type(self.__json_data,"is_baby",bool)
    
    @property
    def species(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"species",NamedAPIResource)
    
    @property
    def evolution_details(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"evolution_details",EvolutionDetail)
    
    @property
    def evolves_to(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"evolves_to",ChainLink)
    
class EvolutionDetail:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def item(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"item",NamedAPIResource)
    
    @property
    def trigger(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"trigger",NamedAPIResource)
    
    @property
    def gender(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"gender",int)
    
    @property
    def held_item(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"held_item",NamedAPIResource)
    
    @property
    def known_move(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"known_move",NamedAPIResource)
    
    @property
    def known_move_type(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"known_move_type",NamedAPIResource)
    
    @property
    def location(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"location",NamedAPIResource)
    
    @property
    def min_level(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"min_level",int)
  
    @property
    def min_happiness(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"min_happiness",int)
 
    @property
    def min_beauty(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"min_beauty",int)
 
    @property
    def min_affection(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"min_affection",int)
   
    @property
    def needs_overworld_rain(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"needs_overworld_rain",int)
    
    @property
    def party_species(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"party_species",NamedAPIResource)
    
    @property
    def party_type(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"party_type",NamedAPIResource)
    
    @property
    def relative_physical_stats(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"relative_physical_stats",int)
   
    @property
    def time_of_day(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"time_of_day",str)
   
    @property
    def trade_species(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"trade_species",NamedAPIResource)
   
    @property
    def turn_upside_down(self) -> Union[bool,None]:
        return Functions.convert_to_type(self.__json_data,"turn_upside_down",bool)
   
class EvolutionChain(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/evolution-chain/" + str(id))
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def baby_trigger_item(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"baby_trigger_item",NamedAPIResource)
    
    @property
    def chain(self) -> Union[ChainLink,None]:
        return Functions.convert_to_type(self._json_data,"chain",ChainLink)