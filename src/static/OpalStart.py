
import json
import os
import sys


class workspace(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


class OpalStart(json.JSONEncoder):
#     __getattr__ = dict.__getitem__
#     __setattr__ = dict.__setitem__

    def __init__(self, platform=None, path=None, workspace=None):
        '''
        Constructor
        '''
        if not workspace:
            workspaceList = list()
            workspace = {}
            workspace['platform'] = platform
            lst = list()
            lst.append(path)
            workspace['path'] = lst
            workspaceList.append(workspace)
        else:
            print 'init', workspace
        self.workspace = workspaceList

    def objToJson(self):
        print 'to_json',self.__dict__
        return json.dumps(self.__dict__)

    @classmethod
    def jsonToObject(cls, json_str):
        json_dict = json.loads(json_str)
        print 'from_json',json_dict
#         for workspace in json_dict:
#             print workspace
        val=cls(**json_dict)
        return val

    @classmethod
    def _dict_to_obj(cls, json_dict):
        for worker in json_dict:
            print worker


if __name__ == "__main__":
#     o = OpalStart(platform=sys.platform, path="/docs/new")
#     print o.objToJson()
    jsonFileStr=''
    f = open(os.path.dirname(__file__) + os.sep + 'opal_start.json', 'r')
    for x in f:
        jsonFileStr=jsonFileStr+x
    f.close()
    print jsonFileStr

#     d=json.loads(jsonFileStr)
#     val=d['workspace']
#     for v in val:
#         s=workspace(v)
#         print s
# #     f.write(json.dumps(book.__dict__, sort_keys=False, indent=4))
# #     f.close()
# #     with open(os.path.dirname(__file__) + os.sep + 'opal_start.json', "r") as jsonFile:
# #         jsonFileStr=jsonFile
#     xx=OpalStart.jsonToObject(jsonFileStr)
#     print xx


    pass
