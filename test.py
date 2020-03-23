import os
import unittest
from datetime import datetime

from main import parse_gedcom
from family import Family
from individual import Individual
from marriage_checkers import is_alive, bigamy, first_cousins_married, check_sibling_counts, check_marriage_aunts_uncles, marriage_before_divorce, marriage_before_death, divorce_before_death, marriages_to_children, marriages_to_siblings

from US_25 import US_25
from US_42 import check_and_convert_string_to_date

from US16_21 import check_correct_gender, check_last_names
from US35_36 import recent_births,recent_deaths

from datescheck import check_BirthDate, check_MarriageDate, check_DivorceDate, check_DeathDate, check_BirthBeforeMarriage, check_BirthBeforeDeath, check_BirthBeforeMarriageOfParents, check_BirthAfterDivorceOfParents
from name_birth import unique_name_and_birth
from US31_32 import multiple_birth, listLivingSingle


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
                         'ANOMALY: INDIVIDUAL: US11, line {22, 23}, Noah Ferris has more than 1 active marriages!'])

    def test_US_19(self):
        file_name = 'US_19.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families, tag_positions = parse_gedcom(
            file_path, 'outputs/test_output.txt')

        self.assertEqual(first_cousins_married(individuals, families, tag_positions), [
                         'ANOMALY: FAMILY: US19, line {56, 50, 75, 76} Cousin 2 is married to his first cousin Cousin 1!'])

    def test_US_16(self):
        file_name = 'US_16.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families, tag_positions = parse_gedcom(
            file_path, 'outputs/test_output.txt')
        self.assertEqual(check_last_names(individuals, families, tag_positions), [
            'ANOMALY: INDIVIDUAL: US16, line {29, 15}, Amit Shah last name is diffrent than Noah Millow last name'])

    def test_US_21(self):
        file_name = 'US_21.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families, tag_positions = parse_gedcom(
            file_path, 'outputs/test_output.txt')
        self.assertEqual(check_correct_gender(individuals, families, tag_positions), [
                         'ANOMALY: INDIVIDUAL: US21, line {19}, Noah Millow has different gender than expected', 'ANOMALY: INDIVIDUAL: US21, line {33}, Amit Millow has different gender than expected'])

    def test_US_01(self):
        file_name = 'US_01,US_02.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families, tag_positions = parse_gedcom(
            file_path, 'outputs/test_output.txt')
        self.assertEqual(check_BirthDate(individuals, tag_positions), [
                         'ANOMALY: INDIVIDUAL: US01, line {147},Sofia Milano is born after current date'])
        self.assertEqual(check_MarriageDate(families, tag_positions), [
                         'ANOMALY: FAMILY: US01, line {232},Oscar Milano and Emma Broadway are married after current date'])
        self.assertEqual(check_DivorceDate(families, tag_positions), [
                         'ANOMALY: FAMILY: US01, line {241},Oscar Milano and Joan Watson are divorced after current date'])
        self.assertEqual(check_DeathDate(individuals, tag_positions), [
                         'ANOMALY: INDIVIDUAL: US01, line {102},Maria Ferrari died after current date'])

    def test_US_02(self):
        file_name = 'US_01,US_02.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families, tag_positions = parse_gedcom(
            file_path, 'outputs/test_output.txt')
        self.assertEqual(check_BirthBeforeMarriage(individuals, families, tag_positions), [
                         'ANOMALY: FAMILY: US02, line {256, 91},Roberto Milano Married before birth'])

    def test_US_23(self):
        file_name = 'US_23.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families, tag_positions = parse_gedcom(
            file_path, 'outputs/test_output.txt')
        self.assertEqual(unique_name_and_birth(individuals, tag_positions), [
                         'ANOMALY: INDIVIDUAL: US23, line {53, 15}, Hp Pate has similar name and birthdate.'])

    def test_US_25(self):
        file_name = 'US_25.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families, tag_positions = parse_gedcom(
            file_path, 'outputs/test_output.txt')

        self.assertEqual(US_25(individuals, families, tag_positions), ['ANOMALY: US25: line {69, 15}, There are multiple Hp Pate in the family.',
                                                                       'ANOMALY: US25: line {74, 20}, There are multiple people born on Jan 02 1970 in the family.'])

    def test_US_42(self):
        self.assertEqual(check_and_convert_string_to_date(
            "30 Feb 1970", 0), None)
        self.assertEqual(check_and_convert_string_to_date(
            "20 Jan 1970", 0), datetime(1970, 1, 20, 0, 0))
        self.assertNotEqual(check_and_convert_string_to_date(
            "20 Jan 1970", 0), datetime(1970, 1, 19, 0, 0))

    # Sprint 2
    def test_US_15(self):
        file_name = 'US_15_False.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families, tag_positions = parse_gedcom(
            file_path, 'outputs/test_output.txt')

        file_name = 'US_15_True.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals2, families2, tag_positions2 = parse_gedcom(
            file_path, 'outputs/test_output.txt')

        self.assertEqual(check_sibling_counts(
            individuals, families, tag_positions), [])
        self.assertEqual(check_sibling_counts(individuals2, families2, tag_positions2), [
                         'ANOMALY: FAMILY: US15, line [27, 31, 35, 39, 43, 47, 51, 55, 59, 63, 67, 71, 75, 79, 83, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101] Family @F1@ has more than 14 siblings!'])

    def test_US_20(self):
        file_name = 'US_20.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families, tag_positions = parse_gedcom(
            file_path, 'outputs/test_output.txt')

        self.assertEqual(check_marriage_aunts_uncles(individuals, families, tag_positions), [
                         'ANOMALY: FAMILY: US20, line{30} Daughter married to their uncle or aunt.', 'ANOMALY: FAMILY: US20, line{36} Son married to their uncle or aunt.'])

    def test_US_04(self):
        file_name = 'US_04_05_06.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families, tag_positions = parse_gedcom(
            file_path, 'outputs/test_output.txt')

        family = Family(1)
        family.divorced = check_and_convert_string_to_date("05 JAN 2005", 0)
        family.married = check_and_convert_string_to_date("10 JAN 2005", 0)
        self.assertEqual(marriage_before_divorce({}, {1: family}, {1: {'DIV': {1}, 'MARR': {2}}}), [
                         'ANOMALY: FAMILY: US04, line{1, 2}, Divorced before marriage in family 1.'])
        self.assertEqual(marriage_before_divorce(individuals, families, tag_positions), [
                         'ANOMALY: FAMILY: US04, line{33, 35}, Divorced before marriage in family @F1@.'])

    def test_US_05(self):
        file_name = 'US_04_05_06.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families, tag_positions = parse_gedcom(
            file_path, 'outputs/test_output.txt')

        self.assertEqual(marriage_before_death(individuals, families, tag_positions), [
                         'ANOMALY: INDIVIDUAL: US05, line {33, 20}, Chris Something was married after their death.'])

    def test_US_06(self):
        file_name = 'US_04_05_06.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families, tag_positions = parse_gedcom(
            file_path, 'outputs/test_output.txt')

        self.assertEqual(divorce_before_death(individuals, families, tag_positions), [
                         'ANOMALY: INDIVIDUAL: US06, line {35, 20}, Chris Something was divorced after their death.'])

    def test_US_17(self):
        file_name = 'US_17_18.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families, tag_positions = parse_gedcom(
            file_path, 'outputs/test_output.txt')

        self.assertEqual(marriages_to_children(individuals, families, tag_positions), [
                         'ANOMALY: FAMILY: US17, line {18, 19}, Father is married to their child(ren) @I3@!'])

    def test_US_18(self):
        file_name = 'US_17_18.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families, tag_positions = parse_gedcom(
            file_path, 'outputs/test_output.txt')

        self.assertEqual(marriages_to_siblings(individuals, families, tag_positions), [
                         'ANOMALY: FAMILY: US18, line {36, 29, 30}, Brother and Daughter are siblings and married to each other!'])

    def test_US_22(self):
        file_name = 'US_22.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families, tag_positions = parse_gedcom(
            file_path, 'outputs/test_output.txt')

    def test_US_35(self):
        file_name='US_35_36.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families, tag_positions = parse_gedcom(
            file_path, 'outputs/test_output.txt')
        self.assertEqual(recent_births(individuals,tag_positions),['ANOMALY: INDIVIDUAL: US35, line {55}, Praj Shah has most recent birthday.', 'ANOMALY: INDIVIDUAL: US35, line {64}, Waah Shah has most recent birthday.'])

    def test_US_31(self):
        file_name = 'US_31.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families, tag_positions = parse_gedcom(
            file_path, 'outputs/test_output.txt')
        self.assertEqual(listLivingSingle(individuals, families, tag_positions), [
                         'Kevin Millow is over 30 years and still not married'])


    def test_US_36(self):
        file_name='US_35_36.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families, tag_positions = parse_gedcom(
            file_path, 'outputs/test_output.txt')
        self.assertEqual(recent_deaths(individuals,tag_positions),['ANOMALY: INDIVIDUAL: US35, line {84}, Raj Shah has most recent death.', 'ANOMALY: INDIVIDUAL: US35, line {100}, Prem Shah has most recent death.'])

    def test_US_32(self):
        file_name = 'US_32.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families, tag_positions = parse_gedcom(
            file_path, 'outputs/test_output.txt')
        self.assertEqual(multiple_birth(individuals, families, tag_positions), [
                    "ANOMALY: FAMILY: US32, ['Amit Shah', 'Kevin Millow'] The two or more individuals were born at the same time"])
    
    def test_US_03(self):
        file_name = 'US_03_US_08.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families, tag_positions = parse_gedcom(
            file_path, 'outputs/test_output.txt')
        self.assertEqual(check_BirthBeforeDeath(individuals, tag_positions), [
              'ANOMALY: Individual: US03, line {64, 66},Parth Shah died before birth'])
    
    def test_US_08(self):
        file_name = 'US_03_US_08.ged'
        file_path = os.path.join(
            current_directory, 'gedcom_test_files', file_name)
        individuals, families, tag_positions = parse_gedcom(
            file_path, 'outputs/test_output.txt')
        self.assertEqual(check_BirthBeforeMarriageOfParents(individuals,families ,tag_positions), [
        'ANOMALY: FAMILY: US08, line {40},Samir Shah was born before marriage of parents'])
        self.assertEqual(check_BirthAfterDivorceOfParents(individuals,families ,tag_positions), [
        'ANOMALY: FAMILY: US08, line {56},Raj Shah born more than 9 months after divorce of parents'])

if __name__ == "__main__":
    unittest.main()
