import unittest

from litocate.data.utils import *

class UtilsTestCase(unittest.TestCase):
    def test_keyword_exist(self):
        self.assertTrue(
            keyword_exist('abbc', ['a', 'd'])
        )
        self.assertFalse(
            keyword_exist('abbc', ['d'])
        )

    def test_compound_keyword_match(self):
        self.assertTrue(
            compound_keyword_match('Abbc', [['a', 'd'], ['b']])
        )
        self.assertFalse(
            compound_keyword_match('abbc', [['a', 'd'], ['e']])
        )

    def test_compound_token_match(self):
        self.assertTrue(
            compound_token_match('A b b c', [['a b', 'd'], ['b']])
        )
        self.assertFalse(
            compound_token_match('a b b c', [['a', 'd'], ['e']])
        )

if __name__=='__main__':
    unittest.main()