import os
import unittest
from datetime import datetime

from main import parse_gedcom
from family import Family
from individual import Individual
from marriage_checkers import is_alive, bigamy, first_cousins_married

from US_25 import US_25
from US_42 import check_and_convert_string_to_date

from US16_21 import check_correct_gender, check_last_names

from datescheck import check_BirthDate, check_MarriageDate, check_DivorceDate, check_DeathDate, check_BirthBeforeMarriage
from name_birth import unique_name_and_birth


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
        individuals, families, tag_positions = parse_gedcom(
            file_path, 'outputs/test_output.txt')

        # Arya and Noah ferris have both been married twice. Arya's partner passed
        # away so she is fine(in a monogamous marriage)! Noah should not be(bigamy).
        self.assertEqual(bigamy(individuals, families, tag_positions), [
                         'ANOMALY: FAMILY: US11, line {22, 23}, Noah Ferris has more than 1 active marriages!'])

    def test_US_19(self):
        file_name = 'US_19.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families, tag_positions = parse_gedcom(
            file_path, 'outputs/test_output.txt')

        self.assertEqual(first_cousins_married(individuals, families, tag_positions), [
                         'ANOMALY: FAMILY: US19, line {56, 50, 75, 76} Cousin 2 is married to his first cousin Cousin 1!'])

    # def test_US_16(self):
    #     file_name = 'US_16.ged'
    #     file_path = os.path.join(
    #         current_directory, 'gedcom_test_files', file_name)
    #     individuals, families = parse_gedcom(
    #         file_path, 'outputs/test_output.txt')
    #     self.assertEqual(check_last_names(individuals, families), [
    #                      'Amit Shah last name is diffrent than Noah Millow last name'])

    # def test_US_21(self):
    #     file_name = 'US_21.ged'
    #     file_path = os.path.join(
    #         current_directory, 'gedcom_test_files', file_name)
    #     individuals, families = parse_gedcom(
    #         file_path, 'outputs/test_output.txt')
    #     self.assertEqual(check_correct_gender(individuals, families), [
    #                      'Noah Millow has different gender than expected', 'Amit Millow has different gender than expected'])

    def test_US_01(self):
        file_name = 'US_01,US_02.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families, tag_positions = parse_gedcom(
            file_path, 'outputs/test_output.txt')
        self.assertEqual(check_BirthDate(individuals, tag_positions),['ANOMALY: FAMILY: US01, line {60},Shalini Shah is born after current date'])
        self.assertEqual(check_MarriageDate(families, tag_positions),['ANOMALY: FAMILY: US01, line {79},Samir Shah and Shalini Shah are married after current date'])
        self.assertEqual(check_DivorceDate(families, tag_positions),['ANOMALY: FAMILY: US01, line {69},Jesal Shah and Sandhya Jain are divorced after current date'])
        self.assertEqual(check_DeathDate(individuals, tag_positions),['ANOMALY: FAMILY: US01, line {51},Raj Jain died after current date'])
    
    def test_US_02(self):
        file_name = 'US_01,US_02.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families, tag_positions = parse_gedcom(
            file_path, 'outputs/test_output.txt')
        self.assertEqual(check_BirthBeforeMarriage(individuals,families, tag_positions),['ANOMALY: FAMILY: US02, line {60, 79},Shalini Shah Married before birth'])
        
    # def test_US_23(self):
    #     file_name = 'US_23.ged'
    #     file_path = os.path.join(current_directory, 'gedcom_test_files',file_name)
    #     individuals, families = parse_gedcom(file_path, 'outputs/test_output.txt')
    #     self.assertEqual(unique_name_and_birth(individuals),['Hp Pate has similar name and birthdate.','1970-01-02 00:00:00 has more than 1 name.'])


    def test_US_25(self):
        file_name = 'US_25.ged'
        file_path = os.path.join(current_directory, 'gedcom_test_files',file_name)
        individuals, families, tag_positions = parse_gedcom(file_path, 'outputs/test_output.txt')
        
        self.assertEqual(US_25(individuals, families, tag_positions),['ANOMALY: US25: line {15}, There are multiple Hp Pate in the family.',
        'ANOMALY: US25: line {74, 20}, There are multiple people born on Jan 02 1970 in the family.'])

    def test_US_42(self):
        self.assertEqual(check_and_convert_string_to_date("30 Feb 1970"),None)
        self.assertEqual(check_and_convert_string_to_date("20 Jan 1970"), datetime(1970, 1, 20, 0, 0))
        self.assertNotEqual(check_and_convert_string_to_date("20 Jan 1970"), datetime(1970, 1, 19, 0, 0))


if __name__ == "__main__":
    unittest.main()
