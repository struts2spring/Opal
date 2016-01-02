'''
Created on 02-Dec-2015

@author: vijay
'''
import unittest

import datetime
date = datetime.datetime.strptime('2012-02-10', '%Y-%m-%d')
date1 = datetime.datetime.strptime("20090127081040-08'00'"[0:8], '%Y%m%d')
print date1
print date.isoweekday()

class Test(unittest.TestCase):


    def testName(self):

        pass


if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
