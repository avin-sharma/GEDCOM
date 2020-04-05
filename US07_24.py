from datetime import datetime


def age_is_legal(individuals, families, tag_positions):
    warnings = []
    for indi_id in individuals:
        individual = individuals[indi_id]
        if(individual.birth != None):
            age = individual.age
            if int(age) > 150:
                if (individual.alive == True):
                    num1 = tag_positions[indi_id]['BIRT']
                    warnings.append(
                        f'ANAMOLY: INDIVIDUAL: US07, line {num1}, {individual.name} is over 150 years old and alive.')
                elif (individual.alive == False):
                    num1 = tag_positions[indi_id]['BIRT']
                    warnings.append(
                        f'ANAMOLY: INDIVIDUAL: US07, line {num1}, {individual.name} was over 150 years old when he was dead.')
    return warnings


def unique_family_by_spouse(individuals, families, tag_positions):
    warnings = []
    fams = []
    for fam_id in families:
        family = families[fam_id]
        fam = {}
        compare = False
        if family.married != None :
            fam["MARR"] = family.married
            fam["HUSB"] = family.hname
            fam["WIFE"] = family.wname
            compare = True
        if compare:
            if fam in fams:
                num = tag_positions[fam_id]['HUSB'] | tag_positions[fam_id]['WIFE'] | tag_positions[fam_id]['MARR']
                warnings.append(
                        f'ANAMOLY: FAMILY: US24, line {num}, Family contain same husband ({family.hname}), same wife ({family.wname}) and same marraige date ({family.married}) as another family.')
            else:
                fams.append(fam)
    return warnings