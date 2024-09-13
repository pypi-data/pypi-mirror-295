import requests_cache
from typing import List,Type,Union
# requests_cache を有効化
import requests

class Functions:
    def convert_to_type(json_data:dict,key: str,target_type: Type):
        if key in json_data and json_data.get(key) is not None:
            return target_type(json_data.get(key))
        else:
            return None
        
    def convert_to_type_list(json_data:dict,key: str,target_type: Type):
        if key in json_data and json_data.get(key) is not None:
            array : List[target_type] = [target_type(js) for js in json_data.get(key)]
            return array
        else:
            return None
class BaseModel:
    def __init__(self,url):
        self.session = requests_cache.CachedSession('pokemon',expire_after=86400)
        self._json_data : dict | None = self.make_request(url)
        
    def make_request(self,url):
        response = self.session.get(url)
        self._status_code = response.status_code
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"Error: Resource not fount at {url}")
            return None
        else:
            response.raise_for_status()
            
    @property
    def status_code(self):
        return self._status_code
            
            
class APIResource:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def url(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"url",str)
    
class NamedAPIResource:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"name",str)
    
    @property
    def url(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"url",str)
    
class Description:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def description(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"description",str)
    @property
    def language(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"language",NamedAPIResource)

class Effect:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def effect(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"effect",str)
    
    @property
    def language(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"language",NamedAPIResource)
    
class Encounter:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def min_level(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"min_level",int)
    
    @property
    def max_level(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"max_level",int)
    
    @property
    def condition_values(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"condition_values",NamedAPIResource)
    
    @property
    def chance(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"chance",int)
    
    @property
    def method(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"method",NamedAPIResource)
    
class FlavorText:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def flavor_text(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"flavor_text",str)
    
    @property
    def language(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"language",NamedAPIResource)
    
    @property
    def version(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"version",NamedAPIResource)
        return NamedAPIResource(self.__json_data["version"])
   
   
class GenerationGameIndex:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def game_index(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"game_index",int)
    
    @property
    def generation(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"generation",NamedAPIResource)

class MachineVersionDetail:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def machine(self) -> Union[APIResource,None]:
        return Functions.convert_to_type(self.__json_data,"machine",APIResource)
    
    @property
    def version_group(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"version_group",NamedAPIResource)
    
 
class Name:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"name",str)
    
    @property
    def language(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"language",NamedAPIResource)


    
class VerboseEffect:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def effect(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"effect",str)
    
    @property
    def short_effect(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"short_effect",str)
    
    @property
    def language(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"language",NamedAPIResource)
    
class VersionGameIndex:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def game_index(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"game_index",int)
    
    @property
    def version(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"version",NamedAPIResource)
    
class VersionEncounterDetail:
    def __init__(self,json_data):
        self.__json_data = json_data

    
    @property
    def version(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"version",NamedAPIResource)
    
    @property
    def max_chance(self) -> Union[int,None]:
        return Functions.convert_to_type(self.__json_data,"max_chance",int)
    
    @property
    def encounter_details(self) -> Union[List,None]:
        return Functions.convert_to_type_list(self.__json_data,"encounter_details",Encounter)
    
class VersionGroupFlavorText:
    def __init__(self,json_data):
        self.__json_data = json_data

    
    @property
    def text(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"text",str)
    
    @property
    def language(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"language",NamedAPIResource)
    
    @property
    def version_group(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"version_group",NamedAPIResource)
