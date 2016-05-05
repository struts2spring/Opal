from src.static.constant import Workspace
import os


class Missing():
    def __init__(self):
        self.missingListing=list()
        self.directory_name = Workspace().libraryPath
    
    def missingNumbers(self):
        directory_name = Workspace().libraryPath
        os.chdir(directory_name)
        listOfDir = [ name for name in os.listdir(directory_name) if os.path.isdir(os.path.join(directory_name, name)) ]
        if listOfDir:
            listOfDir.sort(key=int)
#         for l in listOfDir:
#             print type(l)
        for l in range(7103, 7035, -1):
            if str(l) not in listOfDir:
                self.missingListing.append(l)
        
        return self.missingListing
    
    def availableNumbers(self):
        listOfDir = [ name for name in os.listdir(self.directory_name) if os.path.isdir(os.path.join(self.directory_name, name)) ]
        if listOfDir:
            listOfDir.sort(key=int)
        return listOfDir
        
if __name__=='__main__':
    missing=Missing()
    missing.missingNumbers()
    print missing.missingListing
    print len(missing.missingListing)
    pass