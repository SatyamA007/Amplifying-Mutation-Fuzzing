import unittest
from suffix_tree import suffix_tree

class Testing(unittest.TestCase):
    def test_1(self):
       suffix_tree("dogHasaPotato")

if __name__ == '__main__':
    unittest.main()
    
#Genrate multiple mutatnts using mutmut for given unit test    
#mutmut run