import os
import unittest

import main as parser

current_directory = os.getcwd()
file_name = 'proj02test.ged'
file_path = os.path.join(current_directory, file_name)

parser.parse_gedcom(file_path, 'outputs/test_output.txt')

class TestGEDCOM(unittest.TestCase):
    
    def test_trial(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()