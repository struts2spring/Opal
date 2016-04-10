import os
import shutil


class BookTerminal():
    '''
    This class has been written to deal with all the terminal operation on book directory 
    '''
    def __init__(self):
        pass
    
    def removeBook(self,bookPath=None):
        '''
        this function remove book directory from workspace
        '''
        if bookPath and os.path.exists(bookPath):
            shutil.rmtree(bookPath)
            print 'deleting path'
        pass