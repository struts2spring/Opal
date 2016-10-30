
import json
import os
import sys
from datetime import datetime




class Preference():
    def __init__(self):
        print 'init'
        self.recordPerPage = 50
        self.isPaginationEnable = True
    def __str__(self):
        rep = self.recordPerPage + self.isPaginationEnable
        return rep
class workspace(json.JSONEncoder):

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
        if obj.has_key('platform'):
            obj['platform'] = str(obj['platform'])
        if obj.has_key('image'):
            obj['image'] = str(obj['image'])
        if obj.has_key('searched'):
            obj['searched'] = str(obj['searched'])
        if obj.has_key('library'):
            obj['library'] = str(obj['library'])
        if obj.has_key('path'):
            obj['path'] = list(obj['path'])
        if obj.has_key('user'):
            obj['user'] = obj['user']._asdict()
        if obj.has_key('createdOn'):
            obj['createdOn'] = obj['createdOn']

        return super(workspace, self).encode(obj)   

class OpalStart():

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
            self.workspace = workspaceList
        else:
            print 'init', workspace
            self.workspace = workspace

    def objToDictionary(self, obj):
        '''
        converting to dictionary object.
        '''
        workspaces = {}
        workspaceList = list()
        for workspaceItem in obj.workspace:
            workspaceItem['createdOn'] = str(datetime.now())
            preference = Preference()
            workspaceItem['Preference'] = preference.__dict__
            workspaceList.append(workspaceItem)
        workspaces['workspace'] = workspaceList
        return workspaces
        

    @classmethod
    def jsonToObject(cls, json_str):
        json_dict = json.loads(json_str)
        val = cls(**json_dict)
        return val

    @classmethod
    def _dict_to_obj(cls, json_dict):
        for worker in json_dict:
            print worker

    def readWorkspace(self):
        '''
        This method will read existing opal_start.json file. 
        It will set path, image directory, searched  to Workspace object.
        '''
        
        rep = ''
#             file = open('opal_start.json', 'r')
        with open(os.path.dirname(__file__) + os.sep + 'opal_start.json', 'r') as f:
            for line in f:
                rep = rep + line
            f.close
        return rep    
            
if __name__ == "__main__":

    jsonFileStr = ''
    f = open(os.path.dirname(__file__) + os.sep + 'opal_start.json', 'r')
    for x in f:
        jsonFileStr = jsonFileStr + x
    f.close()

    opalStart = OpalStart()
    startObject = opalStart.jsonToObject(jsonFileStr)
    print startObject
    jsonData = opalStart.objToDictionary(startObject)
    with open('data.json', 'w') as outfile:
        print jsonData
        outfile.write(json.dumps(jsonData))
#         json.dump(str(jsonData), outfile, sort_keys = True, indent = 4)

    pass
