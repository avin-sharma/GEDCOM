import os

from process_output import save_information, print_tables
from marriage_checkers import bigamy, first_cousins_married
from US_25 import US_25
from US_42 import check_and_convert_string_to_date,convert_date_to_string

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
        0 : {'HEAD', 'TRLR', 'NOTE'},
        1 : {'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV'},
        2 : {'DATE'}
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
    x1 = []
    fp = open(file_path, "r")
    for line in fp:
        x1.append(line)
        #print(line)
    #print("____________________________________________________")
    fw = open("ged1105.ged", "w")
    aa: int = len(x1)
    counter = 0
    for i in range(aa):
        counter = counter + 1
        #print("a")
        fw.write(str(counter) + " " + x1[i])


    #current_directory = os.getcwd()
    #file_name="ged1105.ged"
    #file_path = os.path.join(current_directory, file_name)
    #print("q")
    #fo = open(file_name)
    #for li in fo:
        #print(li)
    individuals, families = parse_gedcom(file_path, 'outputs/output.txt')
    US_25(individuals, families)