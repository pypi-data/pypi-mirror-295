from ..Utility.Common import *
from typing import List

class PokemonSpecies(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/pokemon-species/" + str(id))
        
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
    def gender_rate(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"gender_rate",int)
    
    @property
    def capture_rate(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"capture_rate",int)
    
    @property
    def base_happiness(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"base_happiness",int)
    
    @property
    def is_baby(self) -> Union[bool,None]:
        return Functions.convert_to_type(self._json_data,"is_baby",bool)
    
    @property
    def is_legendary(self) -> Union[bool,None]:
        return Functions.convert_to_type(self._json_data,"is_legendary",bool)
    
    @property
    def is_mythical(self) -> Union[bool,None]:
        return Functions.convert_to_type(self._json_data,"is_mythical",bool)
    
    @property
    def hatch_counter(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"hatch_counter",int)

    @property
    def has_gender_differences(self) -> Union[bool,None]:
        return Functions.convert_to_type(self._json_data,"has_gender_differences",bool)
    
    @property
    def forms_switchable(self) -> Union[bool,None]:
        return Functions.convert_to_type(self._json_data,"forms_switchable",bool)
    
    @property
    def growth_rate(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"growth_rate",NamedAPIResource)
    
    @property
    def pokedex_numbers(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"pokedex_numbers",PokemonSpeciesDexEntry)
    
    @property
    def egg_groups(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"egg_groups",NamedAPIResource)
    
    @property
    def color(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"color",NamedAPIResource)
    
    @property
    def shape(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"shape",NamedAPIResource)
    
    @property
    def evolves_from_species(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"evolves_from_species",NamedAPIResource)
    
    @property
    def evolution_chain(self) -> Union[APIResource,None]:
        return Functions.convert_to_type(self._json_data,"evolution_chain",APIResource)
    
    @property
    def habitat(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"habitat",NamedAPIResource)
    
    @property
    def generation(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"generation",NamedAPIResource)
    
    @property
    def names(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"names",Name)
    
    @property
    def pal_park_encounters(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"pal_park_encounters",PalParkEncounterArea)
    
    @property
    def flavor_text_entries(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"flavor_text_entries",FlavorText)
    
    @property
    def form_descriptions(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"form_descriptions",Description)
    
    @property
    def genera(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"genera",Genus)
    
    @property
    def varieties(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"varieties",PokemonSpeciesVariety)
    
    
class Genus:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def genus(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"genus",str)
    
    @property
    def language(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"language",NamedAPIResource)
    
class PokemonSpeciesDexEntry:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def entry_number(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"entry_number",int)
    
    @property
    def pokedex(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"pokedex",NamedAPIResource)
    
class PalParkEncounterArea:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def base_score(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"base_score",int)
    @property
    def rate(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"rate",int)
    @property
    def area(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"area",NamedAPIResource)
    
class PokemonSpeciesVariety:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def is_default(self) -> Union[bool,None]:
        return Functions.convert_to_type(self.__json_data,"is_default",bool)

    @property
    def pokemon(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"pokemon",NamedAPIResource)