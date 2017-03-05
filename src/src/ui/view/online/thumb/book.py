import json


class Book(dict):
    def __init__(self, *args, **kwargs):
        super(Book, self).__init__(*args, **kwargs)
        self.__dict__ = self
        
class VolumeInfo(dict):
    def __init__(self, *args, **kwargs):
        super(VolumeInfo, self).__init__(*args, **kwargs)
        self.__dict__ = self
        
class SearchInfo(dict):
    def __init__(self, *args, **kwargs):
        super(SearchInfo, self).__init__(*args, **kwargs)
        self.__dict__ = self
        
# class SaleInfo(dict):
#     def __init__(SaleInfo, *args, **kwargs):
#         super(SearchInfo, self).__init__(*args, **kwargs)
#         self.__dict__ = self
#         pass
