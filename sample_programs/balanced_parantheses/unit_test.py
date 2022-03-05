import unittest
from balanced_parantheses import balanced_parantheses

class Testing(unittest.TestCase):
    def test_1(self):
       balanced_parantheses("][[[][]()()")

if __name__ == '__main__':
    unittest.main()
    
#Genrate multiple mutatnts using mutmut for given unit test    
#mutmut run