
import json
import os
import sys
import datetime


# class workspace(dict):
#     __getattr__ = dict.__getitem__
#     __setattr__ = dict.__setitem__


class Preference():
    def __init__(self):
        print 'init'

class workspace(json.JSONEncoder):
    def __init__(self):
        pass
    def default(self, obj):
        print 'workspace.default() called'
        if isinstance(obj, datetime):
            return obj.strftime('dt(%Y-%m-%dT%H:%M:%SZ)')
        elif isinstance(obj, Preference):
            return Preference()
            
    def encode(self, obj):
        """
        encode method gets an original object and returns result string. 
        obj argument will be the object that is passed to json.dumps function
        """
        obj['platform'] = str(obj['platform'])
        obj['image'] = str(obj['image'])
        obj['searched'] = str(obj['searched'])
        obj['library'] = str(obj['library'])
        obj['path'] = list(obj['path'])
#         obj['user'] = obj['user']._asdict()

        return super(workspace, self).encode(obj)   

class OpalStart():
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
            workspace['library'] = 'library'
            workspace['path'] = lst
            workspaceList.append(workspace)
        else:
            print 'init', workspace
        self.workspace = workspaceList

    def objToJson(self):
        print 'to_json', self.__dict__
        return json.dumps(self.__dict__, cls=workspace)

    @classmethod
    def jsonToObject(cls, json_str):
        json_dict = json.loads(json_str)
        print 'from_json', json_dict
#         for workspace in json_dict:
#             print workspace
        val = cls(**json_dict)
        return val

    @classmethod
    def _dict_to_obj(cls, json_dict):
        for worker in json_dict:
            print worker


if __name__ == "__main__":
#     o = OpalStart(platform=sys.platform, path="/docs/new")
#     print o.objToJson()
    jsonFileStr = ''
    f = open(os.path.dirname(__file__) + os.sep + 'opal_start.json', 'r')
    for x in f:
        jsonFileStr = jsonFileStr + x
    f.close()
    a = json.dumps(jsonFileStr, default=workspace.default)
    print a
#     print jsonFileStr

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
