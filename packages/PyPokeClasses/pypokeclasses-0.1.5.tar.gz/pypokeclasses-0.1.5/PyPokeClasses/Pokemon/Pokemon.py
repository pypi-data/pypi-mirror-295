from ..Utility.Common import *
from typing import List,Union

class PokemonAbility:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def is_hidden(self) -> Union[bool,None]:
        return Functions.convert_to_type(self.__json_data,"is_hidden",bool)
    
    @property
    def slot(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"slot",int)
    
    @property
    def ability(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"ability",NamedAPIResource)
    
class PokemonType:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def slot(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"slot",int)
    
    @property
    def type(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"type",NamedAPIResource)
    
class PokemonFormType:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def slot(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"slot",int)
    
    @property
    def type(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"type",NamedAPIResource)
    
class PokemonTypePast:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def generation(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"generation",NamedAPIResource)
    
    @property
    def types(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"types",PokemonType)

class PokemonHeldItem:
    def __init__(self,json_data):
        self.__json_data:dict = json_data
        
    @property
    def item(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"item",NamedAPIResource)
    
    @property
    def version_details(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"version_details",PokemonHeldItemVersion)
    
class PokemonHeldItemVersion:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def version(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"version",NamedAPIResource)
    
    @property
    def rarity(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"rarity",int)
    
class PokemonMove:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def move(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"move",NamedAPIResource)
    
    @property
    def version_group_details(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"version_group_details",PokemonMoveVersion)
    
class PokemonMoveVersion:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def move_learn_method(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"move_learn_method",NamedAPIResource)

    @property
    def version_group(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"version_group",NamedAPIResource)
        
    @property
    def level_learned_at(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"level_learned_at",int)
    
class PokemonStat:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def stat(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"stat",NamedAPIResource)
        
    @property
    def effort(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"effort",int)
    
    @property
    def base_stat(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"base_stat",int)

class PokemonSpritesRedBlueYellow:
    def __init__(self,json_data):
        self.__json_data = json_data
    
    @property
    def back_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_default",str)
    
    @property
    def back_gray(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_gray",str)
    
    @property
    def back_transparent(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_transparent",str)
    
    @property
    def front_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_default",str)
    
    @property
    def front_gray(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_gray",str)
    
    @property
    def front_transparent(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_transparent",str)
    
class PokemonSpritesCrystal:
    def __init__(self,json_data):
        self.__json_data = json_data
    
    @property
    def back_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_default",str)
    
    @property
    def back_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_shiny",str)
    
    @property
    def back_shiny_transparent(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_shiny_transparent",str)
    
    @property
    def back_transparent(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_transparent",str)
    
    @property
    def front_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_default",str)
    
    @property
    def front_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny",str)
    
    @property
    def front_shiny_transparent(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny_transparent",str)
    
    @property
    def front_transparent(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_transparent",str)

class PokemonSpritesGoldSilver:
    def __init__(self,json_data):
        self.__json_data = json_data
    
    @property
    def back_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_default",str)
    
    @property
    def back_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_shiny",str)
    
    @property
    def front_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_default",str)
    
    @property
    def front_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny",str)
    
    @property
    def front_transparent(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_transparent",str)
    
class PokemonSpritesEmerald:
    def __init__(self,json_data):
        self.__json_data = json_data
    
    @property
    def front_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_default",str)
    
    @property
    def front_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny",str)
    
class PokemonSpritesFRRG:
    def __init__(self,json_data):
        self.__json_data = json_data

    @property
    def back_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_default",str)
    
    @property
    def back_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_shiny",str)
     
    @property
    def front_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_default",str)
    
    @property
    def front_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny",str)
    
class PokemonSpritesRS:
    def __init__(self,json_data):
        self.__json_data = json_data

    @property
    def back_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_default",str)
    
    @property
    def back_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_shiny",str)
     
    @property
    def front_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_default",str)
    
    @property
    def front_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny",str)
    
class PokemonSpritesDP:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def front_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_default",str)
    
    @property
    def front_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny",str)
    
    @property
    def front_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_female",str)
    
    @property
    def front_shiny_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny_female",str)
    
    @property
    def back_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_default",str)
    
    @property
    def back_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_shiny",str)
    
    @property
    def back_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_female",str)
    
    @property
    def back_shiny_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_shiny_female",str)
    
class PokemonSpritesHGSS:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def front_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_default",str)
    
    @property
    def front_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny",str)
    
    @property
    def front_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_female",str)
    
    @property
    def front_shiny_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny_female",str)
    
    @property
    def back_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_default",str)
    
    @property
    def back_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_shiny",str)
    
    @property
    def back_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_female",str)
    
    @property
    def back_shiny_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_shiny_female",str)

class PokemonSpritesPt:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def front_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_default",str)
    
    @property
    def front_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny",str)
    
    @property
    def front_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_female",str)
    
    @property
    def front_shiny_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny_female",str)
    
    @property
    def back_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_default",str)
    
    @property
    def back_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_shiny",str)
    
    @property
    def back_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_female",str)
    
    @property
    def back_shiny_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_shiny_female",str)
    
class PokemonSpritesAnimated:
    def __init__(self,json_data):
        self.__json_data = json_data
       
    @property
    def front_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_default",str)
    
    @property
    def front_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny",str)
    
    @property
    def front_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_female",str)
    
    @property
    def front_shiny_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny_female",str)
    
    @property
    def back_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_default",str)
    
    @property
    def back_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_shiny",str)
    
    @property
    def back_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_female",str)
    
    @property
    def back_shiny_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_shiny_female",str)
    
class PokemonSpritesBW:
    def __init__(self,json_data):
        self.__json_data = json_data
       
    @property
    def animated(self) -> Union[PokemonSpritesAnimated,None]:
        return Functions.convert_to_type(self.__json_data,"animated",PokemonSpritesAnimated)
     
    @property
    def front_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_default",str)
    
    @property
    def front_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny",str)
    
    @property
    def front_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_female",str)
    
    @property
    def front_shiny_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny_female",str)
    
    @property
    def back_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_default",str)
    
    @property
    def back_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_shiny",str)
    
    @property
    def back_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_female",str)
    
    @property
    def back_shiny_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_shiny_female",str)

class PokemonSpritesORAS:
    def __init__(self,json_data):
        self.__json_data = json_data
       
    @property
    def front_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_default",str)
    
    @property
    def front_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny",str)
    
    @property
    def front_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_female",str)
    
    @property
    def front_shiny_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny_female",str)
    
class PokemonSpritesXY:
    def __init__(self,json_data):
        self.__json_data = json_data
       
    @property
    def front_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_default",str)
    
    @property
    def front_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny",str)
    
    @property
    def front_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_female",str)
    
    @property
    def front_shiny_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny_female",str)

class PokemonSpritesUSUM:
    def __init__(self,json_data):
        self.__json_data = json_data
       
    @property
    def front_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_default",str)
    
    @property
    def front_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny",str)
    
    @property
    def front_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_female",str)
    
    @property
    def front_shiny_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny_female",str)

class PokemonSpritesIcons:
    def __init__(self,json_data):
        self.__json_data = json_data
       
    @property
    def front_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_default",str)
    
    @property
    def front_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_female",str)

    
class PokemonSpritesVersionGi:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def red_blue(self) -> Union[PokemonSpritesRedBlueYellow,None]:
        return Functions.convert_to_type(self.__json_data,"red-blue",PokemonSpritesRedBlueYellow)
    
    @property
    def yellow(self) -> Union[PokemonSpritesRedBlueYellow,None]:
        return Functions.convert_to_type(self.__json_data,"yellow",PokemonSpritesRedBlueYellow)

class PokemonSpritesVersionGii:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def crystal(self) -> Union[PokemonSpritesCrystal,None]:
        return Functions.convert_to_type(self.__json_data,"crystal",PokemonSpritesCrystal)
    
    @property
    def gold(self) -> Union[PokemonSpritesGoldSilver,None]:
        return Functions.convert_to_type(self.__json_data,"gold",PokemonSpritesGoldSilver)

    @property
    def silver(self) -> Union[PokemonSpritesGoldSilver,None]:
        return Functions.convert_to_type(self.__json_data,"silver",PokemonSpritesGoldSilver)

class PokemonSpritesVersionGiii:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def emerald(self) -> Union[PokemonSpritesEmerald,None]:
        return Functions.convert_to_type(self.__json_data,"emerald",PokemonSpritesEmerald)
    
    @property
    def firered_leafgreen(self) -> Union[PokemonSpritesFRRG,None]:
        return Functions.convert_to_type(self.__json_data,"firered-leafgreen",PokemonSpritesFRRG)

    @property
    def ruby_sapphire(self) -> Union[PokemonSpritesRS,None]:
        return Functions.convert_to_type(self.__json_data,"ruby-sapphire",PokemonSpritesRS)

class PokemonSpritesVersionGiv:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def diamond_pearl(self) -> Union[PokemonSpritesDP,None]:
        return Functions.convert_to_type(self.__json_data,"diamond-pearl",PokemonSpritesDP)
    
    @property
    def heartgold_soulsilver(self) -> Union[PokemonSpritesHGSS,None]:
        return Functions.convert_to_type(self.__json_data,"heartgold-soulsilver",PokemonSpritesHGSS)

    @property
    def platinum(self) -> Union[PokemonSpritesPt,None]:
        return Functions.convert_to_type(self.__json_data,"platinum",PokemonSpritesPt)
       
class PokemonSpritesVersionGv:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def black_white(self) -> Union[PokemonSpritesBW,None]:
        return Functions.convert_to_type(self.__json_data,"black-white",PokemonSpritesBW)
    
class PokemonSpritesVersionGvi:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def omegaruby_alphasapphire(self) -> Union[PokemonSpritesORAS,None]:
        return Functions.convert_to_type(self.__json_data,"omegaruby-alphasapphire",PokemonSpritesORAS)
    
    @property
    def x_y(self) -> Union[PokemonSpritesXY,None]:
        return Functions.convert_to_type(self.__json_data,"x-y",PokemonSpritesXY)
    
class PokemonSpritesVersionGvii:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def icons(self) -> Union[PokemonSpritesIcons,None]:
        return Functions.convert_to_type(self.__json_data,"icons",PokemonSpritesIcons)
    
    @property
    def ultra_sun_ultra_moon(self) -> Union[PokemonSpritesUSUM,None]:
        return Functions.convert_to_type(self.__json_data,"ultra-sun-ultra-moon",PokemonSpritesUSUM)
    
class PokemonSpritesVersionGviii:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def icons(self) -> Union[PokemonSpritesIcons,None]:
        return Functions.convert_to_type(self.__json_data,"icons",PokemonSpritesIcons)
    
class PokemonSpritesVersion:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def generation_i(self) -> Union[PokemonSpritesVersionGi,None]:
        return Functions.convert_to_type(self.__json_data,"generation-i",PokemonSpritesVersionGi)

    @property
    def generation_ii(self) -> Union[PokemonSpritesVersionGii,None]:
        return Functions.convert_to_type(self.__json_data,"generation-ii",PokemonSpritesVersionGii)

    @property
    def generation_iii(self) -> Union[PokemonSpritesVersionGiii,None]:
        return Functions.convert_to_type(self.__json_data,"generation-iii",PokemonSpritesVersionGiii)

    @property
    def generation_iv(self) -> Union[PokemonSpritesVersionGiv,None]:
        return Functions.convert_to_type(self.__json_data,"generation-iv",PokemonSpritesVersionGiv)

    @property
    def generation_v(self) -> Union[PokemonSpritesVersionGv,None]:
        return Functions.convert_to_type(self.__json_data,"generation-v",PokemonSpritesVersionGv)

    @property
    def generation_vi(self) -> Union[PokemonSpritesVersionGvi,None]:
        return Functions.convert_to_type(self.__json_data,"generation-vi",PokemonSpritesVersionGvi)

    @property
    def generation_vii(self) -> Union[PokemonSpritesVersionGvii,None]:
        return Functions.convert_to_type(self.__json_data,"generation-vii",PokemonSpritesVersionGvii)

    @property
    def generation_viii(self) -> Union[PokemonSpritesVersionGviii,None]:
        return Functions.convert_to_type(self.__json_data,"generation-viii",PokemonSpritesVersionGviii)

class PokemonSprites2:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def front_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_default",str)
    
    @property
    def front_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny",str)
    
    @property
    def front_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_female",str)
    
    @property
    def front_shiny_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny_female",str)
    
    @property
    def back_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_default",str)
    
    @property
    def back_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_shiny",str)
    
    @property
    def back_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_female",str)
    
    @property
    def back_shiny_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_shiny_female",str)

class PokemonSpritesOther:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def dream_world(self) -> Union[PokemonSprites2,None]:
        return Functions.convert_to_type(self.__json_data,"dream_world",PokemonSprites2)
    
    @property
    def home(self) -> Union[PokemonSprites2,None]:
        return Functions.convert_to_type(self.__json_data,"home",PokemonSprites2)
    
    @property
    def official_artwork(self) -> Union[PokemonSprites2,None]:
        return Functions.convert_to_type(self.__json_data,"official-artwork",PokemonSprites2)
    
    @property
    def showdown(self) -> Union[PokemonSprites2,None]:
        return Functions.convert_to_type(self.__json_data,"showdown",PokemonSprites2)
    
class PokemonSprites:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def front_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_default",str)
    
    @property
    def front_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny",str)
    
    @property
    def front_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_female",str)
    
    @property
    def front_shiny_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"front_shiny_female",str)
    
    @property
    def back_default(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_default",str)
    
    @property
    def back_shiny(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_shiny",str)
    
    @property
    def back_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_female",str)
    
    @property
    def back_shiny_female(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"back_shiny_female",str)
    
    @property
    def other(self) -> Union[PokemonSpritesOther,None]:
        return Functions.convert_to_type(self.__json_data,"other",PokemonSpritesOther)
    
    @property
    def versions(self) -> Union[PokemonSpritesVersion,None]:
        return Functions.convert_to_type(self.__json_data,"versions",PokemonSpritesVersion)

class PokemonCries:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def latest(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"latest",str)
        
    @property
    def legacy(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"legacy",str)
    
class Pokemon(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/pokemon/" + str(id))
        
    @property
    def id(self)-> Union[int , None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def name(self) -> Union[str , None]:
        return Functions.convert_to_type(self._json_data,"name",str)
    
    @property
    def base_experience(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"base_experience",int)
    
    @property
    def height(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"height",int)

    @property
    def is_default(self) -> Union[bool,None]:
        return Functions.convert_to_type(self._json_data,"is_default",bool)

    @property
    def order(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"order",int)

    @property
    def weight(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"weight",int)

    @property
    def abilities(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"abilities",PokemonAbility)
    
    @property
    def forms(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"forms",NamedAPIResource)
    
    @property
    def game_indices(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"game_indices",VersionGameIndex)
    
    @property
    def held_items(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"held_items",PokemonHeldItem)
    
    @property
    def location_area_encounters(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"location_area_encounters",str)
    @property
    def moves(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"moves",PokemonMove)
    
    @property
    def past_types(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"past_types",PokemonTypePast)
    
    @property
    def sprites(self) -> Union[PokemonSprites,None]:
        return Functions.convert_to_type(self._json_data,"sprites",PokemonSprites)
    
    @property
    def cries(self) -> Union[PokemonCries,None]:
        return Functions.convert_to_type(self._json_data,"cries",PokemonCries)
    
    @property
    def species(self) -> Union[NamedAPIResource , None]:
        return Functions.convert_to_type(self._json_data,"species",NamedAPIResource)

    @property
    def stats(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"stats",PokemonStat)
    
    @property
    def types(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self._json_data,"types",PokemonType)