import unittest
from balanced_parantheses import balanced_parantheses

class Testing(unittest.TestCase):
    def test_1(self):
       balanced_parantheses("random")

    def test_2(self):
        balanced_parantheses()
    
    def test_3(self):
        balanced_parantheses()

    def test_4(self):
        balanced_parantheses()

    def test_5(self):
        balanced_parantheses()

if __name__ == '__main__':
    unittest.main()
    
#Genrate multiple mutatnts using mutmut for given unit test    
#mutmut run