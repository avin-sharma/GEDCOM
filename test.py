import os
import unittest

from main import parse_gedcom
from family import Family
from individual import Individual
from marriage_checkers import is_alive, bigamy, first_cousins_married
from US16_21 import check_correct_gender, check_last_names

current_directory = os.getcwd()
# file_name = 'proj02test.ged'
# file_path = os.path.join(current_directory, 'gedcom_test_files',file_name)
# parse_gedcom(file_path, 'outputs/test_output.txt')


class TestGEDCOM(unittest.TestCase):

    def test_is_alive(self):
        indi1 = Individual('1')
        indi2 = Individual('2')
        indi1.alive = False
        indi2.alive = True
        individuals = {
            '1': indi1,
            '2': indi2
        }

        self.assertFalse(is_alive(individuals, '1'))
        self.assertTrue(is_alive(individuals, '2'))

    def test_US_11(self):
        file_name = 'US_11.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families = parse_gedcom(
            file_path, 'outputs/test_output.txt')

        # Arya and Noah ferris have both been married twice. Arya's partner passed
        # away so she is fine(in a monogamous marriage)! Noah should not be(bigamy).
        self.assertEqual(bigamy(individuals, families), [
                         'Noah Ferris has more than 1 active marriages!'])

    def test_US_19(self):
        file_name = 'US_19.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families = parse_gedcom(
            file_path, 'outputs/test_output.txt')

        self.assertEqual(first_cousins_married(individuals, families), [
                         'Cousin 2 is married to his first cousin Cousin 1!'])

    def test_US_16(self):
        file_name = 'US_16.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families = parse_gedcom(
            file_path, 'outputs/test_output.txt')
        self.assertEqual(check_last_names(individuals, families), [
                         'Noah Millow ahs different last name than his son Amit Shah'])

    def test_US_21(self):
        file_name = 'US_21.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families = parse_gedcom(
            file_path, 'outputs/test_output.txt')
        self.assertEqual(check_correct_gender(individuals, families), [
                         'Noah Mellow has wrong gender(He is husband and it should be Male), Anita Millow has wrong gender (She is wife and it should be Female)'])


if __name__ == "__main__":
    unittest.main()
