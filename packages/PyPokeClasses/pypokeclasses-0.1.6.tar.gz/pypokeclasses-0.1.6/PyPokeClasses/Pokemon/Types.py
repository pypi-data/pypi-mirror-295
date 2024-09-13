from ..Utility.Common import *
from typing import List

class TypePokemon:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def slot(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"slot",int)
    
    @property
    def pokemon(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"pokemon",NamedAPIResource)
      
    
    
class TypeRelations:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def no_damage_to(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"no_damage_to",NamedAPIResource)
    
    @property
    def half_damage_to(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"half_damage_to",NamedAPIResource)
    
    @property
    def double_damage_to(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"double_damage_to",NamedAPIResource)
    
    @property
    def no_damage_from(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"no_damage_from",NamedAPIResource)
    
    @property
    def half_damage_from(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"half_damage_from",NamedAPIResource)
    
    @property
    def double_damage_from(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"double_damage_from",NamedAPIResource)
    
class TypeRelationsPast:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def generation(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"generation",NamedAPIResource)
    
    @property
    def damage_relations(self) -> Union[TypeRelations,None]:
        return Functions.convert_to_type(self.__json_data,"damage_relations",TypeRelations)

class TypeSpritesNameIcon:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def name_icon(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"name_icon",str)

class TypeSpritesGenerationiii:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def colosseum(self) -> Union[TypeSpritesNameIcon,None]:
        return Functions.convert_to_type(self.__json_data,"colosseum",TypeSpritesNameIcon)
    
    @property
    def emerald(self) -> Union[TypeSpritesNameIcon,None]:
        return Functions.convert_to_type(self.__json_data,"emerald",TypeSpritesNameIcon)
    
    @property
    def firered_leafgreen(self) -> Union[TypeSpritesNameIcon,None]:
        return Functions.convert_to_type(self.__json_data,"firered-leafgreen",TypeSpritesNameIcon)
    
    @property
    def ruby_saphire(self) -> Union[TypeSpritesNameIcon,None]:
        return Functions.convert_to_type(self.__json_data,"ruby-saphire",TypeSpritesNameIcon)
    
    @property
    def xd(self) -> Union[TypeSpritesNameIcon,None]:
        return Functions.convert_to_type(self.__json_data,"xd",TypeSpritesNameIcon)

class TypeSpritesGenerationiv:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def diamond_pearl(self) -> Union[TypeSpritesNameIcon,None]:
        return Functions.convert_to_type(self.__json_data,"diamond-pearl",TypeSpritesNameIcon)
    
    @property
    def heartgold_soulsilver(self) -> Union[TypeSpritesNameIcon,None]:
        return Functions.convert_to_type(self.__json_data,"heartgold-soulsilver",TypeSpritesNameIcon)
    
    @property
    def platinum(self) -> Union[TypeSpritesNameIcon,None]:
        return Functions.convert_to_type(self.__json_data,"platinum",TypeSpritesNameIcon)

class TypeSpritesGenerationv:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def black_2_white_2(self) -> Union[TypeSpritesNameIcon,None]:
        return Functions.convert_to_type(self.__json_data,"black-2-white-2",TypeSpritesNameIcon)

    @property
    def black_white(self) -> Union[TypeSpritesNameIcon,None]:
        return Functions.convert_to_type(self.__json_data,"black-white",TypeSpritesNameIcon)
    
class TypeSpritesGenerationvi:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def omega_ruby_alpha_sapphire(self) -> Union[TypeSpritesNameIcon,None]:
        return Functions.convert_to_type(self.__json_data,"omega-ruby-alpha-sapphire",TypeSpritesNameIcon)

    @property
    def x_y(self) -> Union[TypeSpritesNameIcon,None]:
        return Functions.convert_to_type(self.__json_data,"x-y",TypeSpritesNameIcon)

class TypeSpritesGenerationvii:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def lets_go_pikachu_lets_go_eevee(self) -> Union[TypeSpritesNameIcon,None]:
        return Functions.convert_to_type(self.__json_data,"lets-go-pikachu-lets-go-eevee",TypeSpritesNameIcon)

    @property
    def sun_moon(self) -> Union[TypeSpritesNameIcon,None]:
        return Functions.convert_to_type(self.__json_data,"sun-moon",TypeSpritesNameIcon)
    
    @property
    def ultra_sun_ultra_moon(self) -> Union[TypeSpritesNameIcon,None]:
        return Functions.convert_to_type(self.__json_data,"ultra-sun-ultra-moon",TypeSpritesNameIcon)
    
class TypeSpritesGenerationviii:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def brilliant_diamond_and_shining_pearl(self) -> Union[TypeSpritesNameIcon,None]:
        return Functions.convert_to_type(self.__json_data,"brilliant-diamond-and-shining-pearl",TypeSpritesNameIcon)

    @property
    def legends_arceus(self) -> Union[TypeSpritesNameIcon,None]:
        return Functions.convert_to_type(self.__json_data,"legends-arceus",TypeSpritesNameIcon)
    
    @property
    def sword_shield(self) -> Union[TypeSpritesNameIcon,None]:
        return Functions.convert_to_type(self.__json_data,"sword-shield",TypeSpritesNameIcon)
    
class TypeSpritesGenerationix:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def scarlet_violet(self) -> Union[TypeSpritesNameIcon,None]:
        return Functions.convert_to_type(self.__json_data,"scarlet-violet",TypeSpritesNameIcon)

class TypeSprites:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def generation_iii(self) -> Union[TypeSpritesGenerationiii,None]:
        return Functions.convert_to_type(self.__json_data,"generation-iii",TypeSpritesGenerationiii)
    
    @property
    def generation_iv(self) -> Union[TypeSpritesGenerationiv,None]:
        return Functions.convert_to_type(self.__json_data,"generation-iv",TypeSpritesGenerationiv)
    
    @property
    def generation_v(self) -> Union[TypeSpritesGenerationv,None]:
        return Functions.convert_to_type(self.__json_data,"generation-v",TypeSpritesGenerationv)
    
    @property
    def generation_vi(self) -> Union[TypeSpritesGenerationvi,None]:
        return Functions.convert_to_type(self.__json_data,"generation-vi",TypeSpritesGenerationvi)

    @property
    def generation_vii(self) -> Union[TypeSpritesGenerationvii,None]:
        return Functions.convert_to_type(self.__json_data,"generation-vii",TypeSpritesGenerationvii)

    @property
    def generation_viii(self) -> Union[TypeSpritesGenerationviii,None]:
        return Functions.convert_to_type(self.__json_data,"generation-viii",TypeSpritesGenerationviii)

    @property
    def generation_ix(self) -> Union[TypeSpritesGenerationix,None]:
        return Functions.convert_to_type(self.__json_data,"generation-ix",TypeSpritesGenerationix)
 
    
class Types(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/type/" + str(id))
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"name",str)
    
    @property
    def damage_relations(self) -> Union[TypeRelations,None]:
        return Functions.convert_to_type(self._json_data,"damage_relations",TypeRelations)
    
    @property
    def past_damage_relations(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"past_damage_relations",TypeRelationsPast)

    @property
    def game_indices(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"game_indices",GenerationGameIndex)
    
    @property
    def generation(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"generation",NamedAPIResource)
    
    @property
    def move_damage_class(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"move_damage_class",NamedAPIResource)
    
    @property
    def names(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"names",Name)

    @property
    def pokemon(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"pokemon",TypePokemon)
    
    @property
    def moves(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"moves",NamedAPIResource)
    
    @property
    def sprites(self) -> Union[TypeSprites,None]:
        return Functions.convert_to_type(self._json_data,"sprites",TypeSprites)