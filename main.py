import os

from process_output import save_information, print_tables
from marriage_checkers import bigamy, first_cousins_married, check_sibling_counts, check_marriage_aunts_uncles, marriage_before_divorce, marriage_before_death, divorce_before_death, marriages_to_siblings, marriages_to_children
from US_25 import US_25
from US_38 import US_38
from US_39 import US_39
from US35_36 import recent_births, recent_deaths
from datescheck import check_BirthDate, check_MarriageDate, check_DivorceDate, check_DeathDate, check_BirthBeforeMarriage, check_BirthBeforeDeath, check_BirthBeforeMarriageOfParents, check_BirthAfterDivorceOfParents, check_BirthBeforeDeathOfMother, check_BirthAfterDeathOfFather, check_BirthofParents, check_ParentsNotTooOld, check_MultipleBirths
from US16_21 import check_correct_gender, check_last_names
from name_birth import unique_name_and_birth
from US31_32 import multiple_birth, listLivingSingle
from US_34 import US_34
from US_37 import US_37
from US_26_33 import corresponding_entries,list_orphans
from US07_24 import age_is_legal, unique_family_by_spouse
from US27_30 import listLivingMarried,includeindividualage
from US_28 import US_28
from US_29 import US_29
from US27_30 import listLivingMarried,includeindividualage
from US27_30 import listLivingMarried,includeindividualage
from US27_30 import listLivingMarried,includeindividualage

def parse_gedcom(path, output_path,US_22_error=False):
    """Parses the file"""
    valid_outputs = []
    try:
        with open(path) as fp:
            for num, line in enumerate(fp, 1):
                line = line.strip()
                # print('-->' + line)
                # out.write('-->' + line + '\n')

                level, tag, valid, arguments = check_valid_input(line)
                if valid == 'Y':
                    valid_outputs.append((num, level, tag, arguments))

                # output = '<--{}|{}|{}|{}'.format(level, tag, valid, arguments)
                # out.write(output + '\n')
                # print(output)

            # process the information and save it
            individuals, families, tag_positions, error = save_information(
                valid_outputs)
            print('Individuals')
            print(str(print_tables(individuals, 'INDI')))

            print('\nFamilies')
            print(str(print_tables(families, 'FAM')))
            print()
        if US_22_error==True:
            return individuals, families, tag_positions, error
        else:
            return individuals, families, tag_positions

    except FileNotFoundError:
        print('File not found')


def check_valid_input(line):
    """
    Given a GEDCOM line, finds if it has valid tags
    """
    VALID_TAGS = {
        0: {'HEAD', 'TRLR', 'NOTE'},
        1: {'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV'},
        2: {'DATE'}
    }

    line = line.split()
    level = int(line[0])
    valid, arguments, tag = 'N', None, None

    if not level and len(line) == 3 and (line[2] == 'FAM' or line[2] == 'INDI'):
        tag = line[2]
        valid = 'Y'
        arguments = line[1]

    else:
        tag, arguments = line[1], ' '.join(line[2:])
        if level < 3 and tag in VALID_TAGS[level]:
            valid = 'Y'

    return level, tag, valid, arguments


if __name__ == "__main__":
    current_directory = os.getcwd()
    file_name = 'family.ged'
    file_path = os.path.join(current_directory, file_name)

    individuals, families, tag_positions, error= parse_gedcom(
        file_path, 'outputs/output.txt', True)

    for warning in bigamy(individuals, families, tag_positions):
        print(warning)  # Oscar Milano

    for warning in first_cousins_married(individuals, families, tag_positions):
        print(warning)

    for warning in check_BirthDate(individuals, tag_positions):
        print(warning)
    for warning in check_MarriageDate(families, tag_positions):
        print(warning)
    for warning in check_DivorceDate(families, tag_positions):
        print(warning)
    for warning in check_DeathDate(individuals, tag_positions):
        print(warning)
    for warning in check_BirthBeforeMarriage(individuals, families, tag_positions):
        print(warning)

    for warning in check_correct_gender(individuals, families, tag_positions):
        print(warning)

    for warning in check_last_names(individuals, families, tag_positions):
        print(warning)

    for warning in unique_name_and_birth(individuals, tag_positions):
        print(warning)

    for warning in US_25(individuals, families, tag_positions):
        print(warning)

    # Sprint 2

    # User Story 15
    for warning in check_sibling_counts(individuals, families, tag_positions):
        print(warning)

    # User Story 20
    for warnings in check_marriage_aunts_uncles(individuals, families, tag_positions):
        print(warnings)

    # User Story 04
    for warnings in marriage_before_divorce(individuals, families, tag_positions):
        print(warnings)

    # User Story 05
    for warnings in marriage_before_death(individuals, families, tag_positions):
        print(warnings)

    # User Story 06
    for warnings in divorce_before_death(individuals, families, tag_positions):
        print(warnings)

    # User Story 38
    for warnings in US_38(individuals, families, tag_positions):
        print(warnings)

    # User Story 39
    for warnings in US_39(individuals, families, tag_positions):
        print(warnings)

    # User Story 35_36
    for warnings in recent_births(individuals, tag_positions):
        print(warnings)

    for warnings in recent_deaths(individuals, tag_positions):
        print(warnings)

    # User Story 03
    for warnings in check_BirthBeforeDeath(individuals, tag_positions):
        print(warnings)
    # User Story 08
    for warnings in check_BirthBeforeMarriageOfParents(individuals, families, tag_positions):
        print(warnings)
    # User Story 08
    for warnings in check_BirthAfterDivorceOfParents(individuals, families, tag_positions):
        print(warnings)
    # User Story 31
    for warnings in multiple_birth(individuals, families, tag_positions):
        print(warnings)
    # User Story 32
    for warning in listLivingSingle(individuals, families, tag_positions):
        print(warning)
    
    # User Story 07
    for warning in age_is_legal(individuals, families, tag_positions):
        print(warning)
    # User Story 24
    for warning in unique_family_by_spouse(individuals, families, tag_positions):
        print(warning)

    # User Story 34
    for warning in US_34(individuals, families, tag_positions):
        print(warning)

    # User Story 37
    for warning in US_37(individuals, families, tag_positions):
        print(warning)
    # User Story 33
    for warnings in list_orphans(individuals,families,tag_positions):
        print(warnings)
    #User Story 26
    for warnings in corresponding_entries(individuals,families,tag_positions):
        print(warnings)
    #User Story 09
    for warning in check_BirthBeforeDeathOfMother(individuals,families, tag_positions):
        print(warning)
    #User Story 09
    for warning in check_BirthAfterDeathOfFather(individuals,families, tag_positions):
        print(warning)
    #User Story 10
    for warning in check_BirthofParents(individuals,families, tag_positions):
        print(warning)
    
    # User Story 17
    for warnings in marriages_to_children(individuals, families, tag_positions):
        print(warnings)

    #User Story 18
    for warning in marriages_to_siblings(individuals,families,tag_positions):
        print(warning)

    #User Story 22
    print(error)

    #User Story 12
    for warning in check_ParentsNotTooOld(individuals,families, tag_positions):
        print(warning)
    #User Story 14
    for warning in check_MultipleBirths(individuals,families, tag_positions):
        print(warning)
    # User Story 27
    for warnings in includeindividualage(individuals,families,tag_positions):
        print(warnings)
    # User Story 30
    for warnings in listLivingMarried(individuals,families,tag_positions):
        print(warnings)
    # User Story 28
    for warnings in US_28(individuals, families, tag_positions):
        print(warnings)
    # User Story 29
    for warnings in US_29(individuals, families, tag_positions):
        print(warnings)

