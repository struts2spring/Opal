from src.dao.online.OnlineBookDaoImpl import OnlineDatabase


class OnlineBookInfoLogic():
    
    def __init__(self):
        self.onlineDatabase = OnlineDatabase()
        pass
    
    def bookListInOnlineDatabase(self, isbnList):
        '''
        This function return list of books that is not available in database, 
        from the list that have been provided as an input.
        '''
        result = self.onlineDatabase.findIsbnList(isbnList)
        pureList = list(val[0] for val in result)
        return pureList
    
    def bookListNotInOnlineDatabase(self, isbnList):
        '''
        This function return list of books that is not available in database, 
        from the list that have been provided as an input.
        '''
        pureList = self.bookListInOnlineDatabase(isbnList)
        resultList = self.removeAll(fistList=isbnList, secondList=pureList)
        return resultList
        
    def removeAll(self, fistList=None, secondList=None):
        
        result = list(set(fistList) - set(secondList)) 
        return result
    
    def getBookInfoObjects(self, isbnList):
        result = self.onlineDatabase.findBookInfo(isbnList)
        return result

if __name__ == '__main__':
    isbnList = ['11111', '22222', '0596009208', 'B01BYGN93S', '0321356683', '0134177304', '1118407814', '1530011396', '0672337029', '1449370829', '1119272092']
    secondList = ['0596009208', 'B01BYGN93S']
    onlineBookInfoLogic = OnlineBookInfoLogic()
#     finalList=onlineBookInfoLogic.removeAll(isbnList, secondList)
#     print finalList
    
    result = onlineBookInfoLogic.bookListNotInOnlineDatabase(isbnList)

#     finalList=onlineBookInfoLogic.removeAll(isbnList, resultList)
    print result
    pass
