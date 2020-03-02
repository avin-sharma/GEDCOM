from datetime import datetime


def check_correct_gender(individuals, families):
    warnings = set()
    for family in families.values():
        for indi_id in individuals:
            individual = individuals[indi_id]
            if (family.hid == indi_id):
                hus_sex = individual.gender
                if(hus_sex != "M"):
                    warnings.add(
                        f'{individual.name} has different gender than expected')
            elif (family.wid != indi_id):
                wife_sex = individual.gender
                if(wife_sex != "F"):
                    warnings.add(
                        f'{individual.name} has different gender than expected')
    return warnings


def get_last_name(name):
    return name.split()[1]


def check_last_names(individuals, families):
    warnings = []
    for family in families.values():
        husband_last_name = get_last_name(family.hname)
        for i in family.children:
            for indi_id in individuals:
                individual = individuals[indi_id]
                if(i == indi_id):
                    if (individual.gender == "M"):
                        if husband_last_name is None:
                            husband_last_name = get_last_name(individual.name)
                        else:
                            if husband_last_name != get_last_name(individual.name):
                                warnings.append(
                                    f'{individual.name} last name is diffrent than {family.hname} last name')
    return warnings
