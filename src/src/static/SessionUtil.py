from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from src.static.constant import Workspace
import os
from src.dao.Book import Base

class SingletonSession(object):
    
    class __SingletonSession:
        def __init__(self):
            self.createSession()
        def __str__(self):
            return repr(self) + self.val
    
    
        def createSession(self):
            engine = create_engine('sqlite:///' + Workspace().libraryPath + os.sep + '_opal.sqlite', echo=True)
            Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
            self.session = Session()
            database_fileName = os.path.join(Workspace().libraryPath , '_opal.sqlite')
            if not os.path.exists(database_fileName) or os.path.getsize(database_fileName)==0:
                if not os.path.exists(Workspace().libraryPath):
                    os.mkdir(Workspace().libraryPath)
                os.chdir(Workspace().libraryPath)
    #             print '---------------------------',os.path.getsize(database_fileName)
    #             self.creatingDatabase()
                print Base.metadata.drop_all(engine)
                print Base.metadata.create_all(engine)
        
        
    
    instance = None
    def __new__(cls):  # __new__ always a classmethod
        if not SingletonSession.instance:
            SingletonSession.instance = SingletonSession.__SingletonSession()
        return SingletonSession.instance
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name):
        return setattr(self.instance, name)