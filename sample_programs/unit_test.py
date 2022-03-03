import unittest
from crash_me import crash_me

class Testing(unittest.TestCase):
    def test_string(self):
       crash_me("good")

    def test_boolean(self):
        crash_me("bad")

if __name__ == '__main__':
    unittest.main()
    
#Genrate multiple mutatnts using mutmut for given unit test    
#mutmut run