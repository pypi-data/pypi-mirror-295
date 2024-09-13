from ..Utility.Common import *
from typing import List

class ContestComboDetail:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def use_before(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"use_before",NamedAPIResource)
    
    @property
    def use_after(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"use_after",NamedAPIResource)
    
class ContestComboSets:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def normal(self) -> Union[ContestComboDetail,None]:
        return Functions.convert_to_type(self.__json_data,"normal",ContestComboDetail)
    
    @property
    def super(self) -> Union[ContestComboDetail,None]:
        return Functions.convert_to_type(self.__json_data,"super",ContestComboDetail)

    
class MoveFlavorText:
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
    
class MoveMetaData:
    def __init__(self,json_data):
        self.__json_data = json_data
    
    @property
    def ailment(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"ailment",NamedAPIResource)
    
    @property
    def category(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"category",NamedAPIResource)
    
    @property
    def min_hits(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"min_hits",int)
    
    @property
    def max_hits(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"max_hits",int)
    
    @property
    def min_turns(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"min_turns",int)
    
    @property
    def max_turns(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"max_turns",int)
    
    @property
    def drain(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"drain",int)
    
    @property
    def healing(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"healing",int)
    
    @property
    def crit_rate(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"crit_rate",int)
    
    @property
    def ailment_chance(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"ailment_chance",int)
    
    @property
    def flinch_chance(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"flinch_chance",int)
    
    @property
    def stat_chance(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"stat_chance",int)
    
    
class MoveStatChange:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def change(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"change",int)
    
    @property
    def stat(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"stat",NamedAPIResource)
    
class PastMoveStatValues:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def accuracy(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"accuracy",int)
    
    @property
    def effect_chance(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"effect_chance",int)
    
    @property
    def power(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"power",int)
    
    @property
    def pp(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"pp",int)
    

    @property
    def effect_entries(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"effect_entries",VerboseEffect)
    
    @property
    def type(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"type",NamedAPIResource)
    
    @property
    def version_group(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"version_group",NamedAPIResource)
    
class Moves(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/move/" + str(id))
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"name",str)
    
    @property
    def accuracy(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"accuracy",int)
    
    @property
    def effect_chance(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"effect_chance",int)
    
    @property
    def pp(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"pp",int)
    
    @property
    def priority(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"priority",int)
    
    @property
    def power(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"power",int)
    
    @property
    def contest_combos(self) -> Union[ContestComboSets,None]:
        return Functions.convert_to_type(self._json_data,"contest_combos",ContestComboSets)
    
    @property
    def contest_type(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"contest_type",NamedAPIResource)

    @property
    def contest_effect(self) -> Union[APIResource,None]:
        return Functions.convert_to_type(self._json_data,"contest_effect",APIResource)
    
    @property
    def damage_class(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"damage_class",NamedAPIResource)
      
    @property
    def effect_entries(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"effect_entries",VerboseEffect)
    
    @property
    def effect_changes(self) -> Union[List,None]:
        from ..Pokemon.Abilities import AbilityEffectChange
        return Functions.convert_to_type_list(self._json_data,"effect_changes",AbilityEffectChange)
    
    @property
    def learned_by_pokemon(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"learned_by_pokemon",NamedAPIResource)
    
    @property
    def flavor_text_entries(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"flavor_text_entries",MoveFlavorText)
    
    @property
    def generation(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"generation",NamedAPIResource)

    @property
    def machines(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"machines",MachineVersionDetail)
    
    @property
    def meta(self) -> Union[MoveMetaData,None]:
        return Functions.convert_to_type(self._json_data,"meta",MoveMetaData)
    
    @property
    def names(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"names",Name)
    
    @property
    def past_values(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"past_values",PastMoveStatValues)
    
    @property
    def stat_changes(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"stat_changes",MoveStatChange)
    
    @property
    def super_contest_effect(self) -> Union[APIResource,None]:
        return Functions.convert_to_type(self._json_data,"super_contest_effect",APIResource)
    
    @property
    def target(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"target",NamedAPIResource)
    
    @property
    def type(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"type",NamedAPIResource)

