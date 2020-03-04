##US01 : Dates (birth, marriage, divorce, death) should not be after the current date
##US02 : Birth should occur before marriage of an individual
from datetime import datetime
currentDate = datetime.now()
def check_BirthDate(individuals, tag_positions):
##US01 : Dates (birth) should not be after the current date
    warnings = []
    for indi_id in individuals:
        individual = individuals[indi_id]
        if individual.birth != None:
            if individual.birth > currentDate: 
                num = tag_positions[indi_id]['BIRT']
                warnings.append(f'ANOMALY: INDIVIDUAL: US01, line {num},{individual.name} is born after current date')
    return warnings

def check_MarriageDate(families, tag_positions):
##US01 : Dates (marriage) should not be after the current date
    warnings = []
    for fam_id in families:
        family = families[fam_id]
        if family.married:
            if family.married > currentDate:
                num = tag_positions[fam_id]['MARR']
                warnings.append(f'ANOMALY: FAMILY: US01, line {num},{family.hname} and {family.wname} are married after current date')
    return warnings

def check_DivorceDate(families, tag_positions):
##US01 : Dates (divorce) should not be after the current date
    warnings = []
    for fam_id in families:
        family = families[fam_id]
        if family.divorced:
            if family.divorced > currentDate:
                num = tag_positions[fam_id]['DIV']
                warnings.append(f'ANOMALY: FAMILY: US01, line {num},{family.hname} and {family.wname} are divorced after current date')
    return warnings

def check_DeathDate(individuals, tag_positions):
##US01 : Dates (death) should not be after the current date
    warnings = []
    for indi_id in individuals:
        individual = individuals[indi_id]
        if individual.death:
            if individual.death > currentDate:
                num = tag_positions[indi_id]['DEAT']
                warnings.append(f'ANOMALY: INDIVIDUAL: US01, line {num},{individual.name} died after current date')
    return warnings

def check_BirthBeforeMarriage(individuals,families, tag_positions):
##US02 : Birth should occur before marriage of an individual
    warnings = []
    for indi_id in individuals:
        individual = individuals[indi_id]
        for fam_id in individual.spouse:
            family = families[fam_id]
            if individual.birth and family.married:
                if individual.birth > family.married:
                    num = tag_positions[indi_id]['BIRT']|tag_positions[fam_id]['MARR']
                    warnings.append(f'ANOMALY: FAMILY: US02, line {num},{individual.name} Married before birth')
    return warnings