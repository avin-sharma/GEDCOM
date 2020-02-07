import os

import main as parser

current_directory = os.getcwd()
file_name = 'proj02test.ged'
file_path = os.path.join(current_directory, file_name)

parser.parse_gedcom(file_path, 'outputs/test_output.txt')