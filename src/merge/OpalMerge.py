'''
Created on 01-Jul-2017

@author: vijay
'''
import os

import tempfile
import logging.config
from src.logic.ReadWriteJson import ReadWriteJsonInfo

logger = logging.getLogger('extensive')



LOG_SETTINGS = {
'version': 1,
'handlers': {
    'console': {
        'class': 'logging.StreamHandler',
        'level': 'DEBUG',
        'formatter': 'detailed',
        'stream': 'ext://sys.stdout',
    },
    'file': {
        'class': 'logging.handlers.RotatingFileHandler',
        'level': 'DEBUG',
        'formatter': 'detailed',
        'filename': os.path.join(tempfile.gettempdir(),'OpalEbookManager.log'),
        'mode': 'a',
        'maxBytes': 10485760,
        'backupCount': 5,
    },

},
'formatters': {
    'detailed': {
        'format': '%(asctime)s %(module)-17s line:%(lineno)-4d %(levelname)-8s %(message)s',
    },
    'email': {
        'format': 'Timestamp: %(asctime)s\nModule: %(module)s\n' \
        'Line: %(lineno)d\nMessage: %(message)s',
    },
},
'loggers': {
    'extensive': {
        'level':'DEBUG',
        'handlers': ['file','console' ]
        },
}
}
logging.config.dictConfig(LOG_SETTINGS)

class WalkLibrary():
    '''
    This class is to merge two or more library path of Opal Library.
    '''
    def __init__(self):
        self.readWriteJsonInfo=ReadWriteJsonInfo()
        pass
    
    def mergeLibrary(self, libraryPaths):
        pass
    
    def walkDir(self, libraryPath="."):
        listOfDir = list()
        bookList=list()  
        if os.path.exists(libraryPath):
            os.chdir(libraryPath)
#             listOfDir = os.listdir(libraryPath)
            for bookFolder in os.listdir(libraryPath):
                if os.path.isdir(os.path.join(libraryPath, bookFolder)) :
                    try:
                        if int(bookFolder):
                            listOfDir.append(bookFolder)
                            b = self.readWriteJsonInfo.readJsonFromDir(dirName=bookFolder)
                            bookList.append(b)
                    except Exception as e:
                        pass
#                         logger.error(e, exc_info=True)
        if listOfDir:
            listOfDir.sort(key=int)      
            
#         logger.info(len(listOfDir))    
#         logger.info(listOfDir)    
        logger.info(len(bookList))    
                      
if __name__ == '__main__':
    
#     one=[1,2,3,4,5]
#     two=[4,5,6,7,8]
#     print(list(set(one)-set(two)))
    
    WalkLibrary().walkDir(libraryPath='/docs/new/library/')
    pass
