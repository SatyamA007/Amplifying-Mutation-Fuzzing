import unittest
from evaluate_expression import evaluate_expression

class Testing(unittest.TestCase):
    def test_1(self):
       evaluate_expression("2*(5+5*2)/3+(6/2+8)")

    def test_2(self):
        evaluate_expression('2*(5+5*2)/3+(62+8)')
    
    def test_3(self):
        evaluate_expression('1+2*6-3')

if __name__ == '__main__':
    unittest.main()
    
#Genrate multiple mutatnts using mutmut for given unit test    
#mutmut run