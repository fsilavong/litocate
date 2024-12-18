import unittest

from litocate.data.acl import AnthologyClient

class ACLTestCase(unittest.TestCase):
    def test_meet_criteria(self):
        match1 = AnthologyClient._meet_criteria(
            'dummy text', '', ['text'], 2021
        )
        self.assertEqual(match1, False)
        match2 = AnthologyClient._meet_criteria(
            'dummy text', '2023', ['text'], 2021
        )
        self.assertEqual(match2, True)
        match3 = AnthologyClient._meet_criteria(
            'dummy text', '2023', ['text'], 2024
        )
        self.assertEqual(match3, False)
    
    # @patch('Anthology.from_repo', )
    # def test_find_paper(self):
        # client = AnthologyClient()
            
if __name__=='__main__':
    unittest.main()