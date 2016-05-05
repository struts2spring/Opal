import json
import os
from src.static.constant import Workspace

class SearchCache(json.JSONEncoder):
    '''
    This class is going to store all the search result.
    '''
    
    def __init__(self):
        if not os.path.exists(Workspace().library):
            os.mkdir(Workspace().library)
        os.chdir(Workspace().library)
        pass
    

    def objToJson(self):
        print 'to_json', self.__dict__
        return json.dumps(self.__dict__)
    
    @classmethod
    def jsonToObject(cls, json_str):
        json_dict = json.loads(json_str)
        print 'from_json', json_dict
#         for workspace in json_dict:
#             print workspace
        val = cls(**json_dict)
        return val

    def writeJson(self):
        with open(Workspace().library + os.sep + 'opal_cache.json', 'r') as jsonFile:
            jsonFile.write(self.objToJson())

#         jsonFile = open(Workspace().library + os.sep + 'opal_cache.json', 'r')
#         jsonFile.write(json.dumps(self.__dict__, sort_keys=False, indent=4))
#         jsonFile.close()
if __name__ == "__main__":
    searchCache = SearchCache()
    searchCache.writeJson()
