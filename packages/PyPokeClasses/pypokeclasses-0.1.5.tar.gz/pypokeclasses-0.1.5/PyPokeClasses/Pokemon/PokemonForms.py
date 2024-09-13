from ..Utility.Common import *
from typing import List
class PokemonFormSprites:
    def __init__(self,json_data):
        self.__json_data = json_data
        

    @property
    def front_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_default",str)

    @property
    def front_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_female",str)
    
    @property
    def front_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny",str)
    
    @property
    def front_shiny_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny_female",str)
    
    @property
    def back_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_default",str)
    
    @property
    def back_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_female",str)
    
    @property
    def back_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_shiny",str)
    
    @property
    def back_shiny_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_shiny_female",str)
    
class PokemonForms(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/pokemon-form/" + str(id))
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"name",str)
    
    @property
    def order(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"order",int)
    
    @property
    def form_order(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"form_order",int)
    
    @property
    def is_default(self) -> Union[bool,None]:
        return Functions.convert_to_type(self._json_data,"is_default",bool)
    
    @property
    def is_battle_only(self) -> Union[bool,None]:
        return Functions.convert_to_type(self._json_data,"is_battle_only",bool)
    
    @property
    def is_mega(self) -> Union[bool,None]:
        return Functions.convert_to_type(self._json_data,"is_mega",bool)

    @property
    def form_name(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"form_name",str)
    
    @property
    def pokemon(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"pokemon",NamedAPIResource)
    
    @property
    def types(self) -> Union[List,None]:
        from .Pokemon import PokemonFormType
        return Functions.convert_to_type_list(self._json_data,"types",PokemonFormType)
    
    @property
    def sprites(self) -> Union[PokemonFormSprites,None]:
        return Functions.convert_to_type(self._json_data,"sprites",PokemonFormSprites)
    
    @property
    def version_group(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"version_group",NamedAPIResource)
    
    @property
    def names(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"names",Name)
    
    @property
    def form_names(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"form_names",Name)
    
    

    