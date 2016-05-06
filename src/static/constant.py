'''
Created on 02-Dec-2015

@author: vijay
'''
import json
import sys
import os




class Workspace(object):
    '''
    This class help to define workspace location. It is a singleton class.
    '''
    class __Workspace:

        def __init__(self):
            self.readWorkspace()
        def __str__(self):
            return `self` + self.path

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
            # print str(rep)
            opal_start = json.loads(rep)
            for workspace in opal_start['workspace']:
#                 x=OpalStart(workspace)
                print workspace['platform']
                if sys.platform == workspace['platform']:
                    self.path = str(workspace['path'][0])
                    if not os.path.exists(self.path):
                        os.mkdir(self.path)
                    self.libraryPath = os.path.join(str(workspace['path'][0]),workspace['library'])
                    if not os.path.exists(self.libraryPath):
                        os.mkdir(self.libraryPath)
                    self.imagePath = os.path.join(str(workspace['path'][0]),workspace['image'])
                    if not os.path.exists(self.imagePath):
                        os.mkdir(self.imagePath)
                    self.searchedPath = os.path.join(str(workspace['path'][0]),workspace['searched'])
                    if not os.path.exists(self.searchedPath):
                        os.mkdir(self.searchedPath)
            print self.path

        def writeWorkspace(self, newPath=None):
#             print self.opal_start
            if newPath:
                with open(os.path.dirname(__file__) + os.sep + 'opal_start.json', "r") as jsonFile:
                    data = json.load(jsonFile)
                for k in data:
                    print data[k]
                    for d in data[k]:
                        if sys.platform == d['platform']:
                            d['library']='library'
                            d['image']='image'
                            d['searched']='searched'
                            d['path'].insert(0, newPath)
#                             print data[k]['path']
                            self.path = str(d['path'][0])

                with open(os.path.dirname(__file__) + os.sep + 'opal_start.json', "w") as jsonFile:
                    jsonFile.write(json.dumps(data))

    instance = None
    def __new__(cls):  # __new__ always a classmethod
        if not Workspace.instance:
            Workspace.instance = Workspace.__Workspace()
        return Workspace.instance
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name):
        return setattr(self.instance, name)



if __name__ == "__main__":
    x = Workspace()
#     x.path = 'sausage'
#     print(x)
#     y = Workspace()
#     y.path = 'eggs'
#     print(y)
#     z = Workspace()
#     z.path = 'spam'
#     print(z)
#     print(x)
#     print(y)
    x.writeWorkspace("/docs/new")
    print x.libraryPath
    print type(Workspace().path), Workspace().path
