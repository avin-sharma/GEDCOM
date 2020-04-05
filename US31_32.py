from datetime import datetime
from prettytable import PrettyTable


def multiple_birth(individuals, families, tag_positions):
    warnings = []
    dic = {}
    for indi_id in individuals:
        individual = individuals[indi_id]
        if(individual.birth != None):
            dic[individual.name] = individual.birth
    new_dict = {}
    for pair in dic.items():
        if pair[1] not in new_dict.keys():
            new_dict[pair[1]] = []
        new_dict[pair[1]].append(pair[0])
    for k, v in new_dict.items():
        if (len(v) >= 2):
            warnings.append(
                f'ANOMALY: FAMILY: US32, {v} The two or more individuals were born at the same time')
    return warnings


def listLivingSingle(individuals, families, tag_positions):
    warning = []
    for indi_id in individuals:
        individual = individuals[indi_id]
        if(individual.age != None and int(individual.age) > 30 and individual.death == None and len(individual.spouse) == 0):
            num = tag_positions[indi_id]['NAME']
            warning.append(
                f'ANOMALY: INDIVIDUAL: US31,Line {num} {individual.name} is over 30 years and still not married')
    return warning
