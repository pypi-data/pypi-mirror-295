from ..Utility.Common import *
from .BerryFirmness import BerryFirmness
from .BerryFlavor import BerryFlavor
from ..Items.Item import Item
from ..Pokemon.Types import Types
from typing import List

class Berry(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/berry/" + str(id))
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"name",str)
    
    @property
    def growth_time(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"growth_time",int)
    
    @property
    def max_harvest(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"max_harvest",int)
    
    @property
    def natural_gift_power(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"natural_gift_power",int)
    
    @property
    def size(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"size",int)
    
    @property
    def smoothness(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"smoothness",int)
    
    @property
    def soil_dryness(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"soil_dryness",int)
    
    @property
    def firmness(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"firmness",NamedAPIResource)
    
    @property
    def flavors(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"flavors",BerryFlavorMap)
    
    @property
    def item(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"item",NamedAPIResource)
    
    @property
    def natural_gift_type(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"natural_gift_type",NamedAPIResource)
    
class BerryFlavorMap:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def potency(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"potency",int)
    
    @property
    def flavor(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"flavor",NamedAPIResource)
    