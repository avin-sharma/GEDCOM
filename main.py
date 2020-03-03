import os

from process_output import save_information, print_tables
from marriage_checkers import bigamy, first_cousins_married
from US_25 import US_25


from datescheck import check_BirthDate, check_MarriageDate, check_DivorceDate, check_DeathDate, check_BirthBeforeMarriage
from US16_21 import check_correct_gender, check_last_names

from name_birth import unique_name_and_birth


def parse_gedcom(path, output_path):
    """Parses the file"""
    valid_outputs = []
    try:
        with open(path) as fp, open(output_path, 'w') as out:
            for line in fp:
                line = line.strip()
                # print('-->' + line)
                # out.write('-->' + line + '\n')

                level, tag, valid, arguments = check_valid_input(line)
                if valid == 'Y':
                    valid_outputs.append((level, tag, arguments))

                # output = '<--{}|{}|{}|{}'.format(level, tag, valid, arguments)
                # out.write(output + '\n')
                # print(output)

            # process the information and save it
            individuals, families = save_information(valid_outputs)
            out.write('Individuals\n')
            out.write(str(print_tables(individuals, 'INDI')))
            out.write('\n\nFamilies\n')
            out.write(str(print_tables(families, 'FAM')))

        return individuals, families

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
    file_name = 'test.ged'
    file_path = os.path.join(current_directory, file_name)
    individuals, families = parse_gedcom(file_path, 'outputs/output.txt')
    
    for warnings in US_25(individuals, families) :
        print(f"This name and birthday of child {warnings} have duplicate values")

    for warning in bigamy(individuals, families):
        print(warning)  # Oscar Milano

    for warning in first_cousins_married(individuals, families):
        print(warning)
    
    for warning in check_BirthDate(individuals):
        print(warning)
    for warning in check_MarriageDate(families):
        print(warning)
    for warning in check_DivorceDate(families):
        print(warning)
    for warning in check_DeathDate(individuals):
        print(warning)
    for warning in check_BirthBeforeMarriage(individuals,families):
        print(warning)
    

    for warning in check_correct_gender(individuals, families):
        print(warning)

    for warning in check_last_names(individuals, families):
        print(warning)

    for warning in unique_name_and_birth(individuals):
        print(warning)

