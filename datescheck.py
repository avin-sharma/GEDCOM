##US01 : Dates (birth, marriage, divorce, death) should not be after the current date
##US02 : Birth should occur before marriage of an individual
from datetime import datetime
currentDate = datetime.now()
def check_BirthDate(individuals):
##US01 : Dates (birth) should not be after the current date
    warnings = []
    for indi_id in individuals:
        individual = individuals[indi_id]
        if individual.birth != None:
            if individual.birth > currentDate: 
                warnings.append(f'{individual.name} is born after current date')
    return warnings

def check_MarriageDate(families):
##US01 : Dates (marriage) should not be after the current date
    warnings = []
    for fam_id in families:
        family = families[fam_id]
        if family.married != None:
            if family.married > currentDate:
                warnings.append(f'{family.hname} and {family.wname} are married after current date')
    return warnings

def check_DivorceDate(families):
##US01 : Dates (divorce) should not be after the current date
    warnings = []
    for fam_id in families:
        family = families[fam_id]
        if family.divorced != None:
            if family.divorced > currentDate:
                warnings.append(f'{family.hname} and {family.wname} are divorced after current date')
    return warnings

def check_DeathDate(individuals):
##US01 : Dates (death) should not be after the current date
    warnings = []
    for indi_id in individuals:
        individual = individuals[indi_id]
        if individual.death != None:
            if individual.death > currentDate:
                warnings.append(f'{individual.name} died after current date')
    return warnings

def check_BirthBeforeMarriage(individuals,families):
##US02 : Birth should occur before marriage of an individual
    warnings = []
    for indi_id in individuals:
        individual = individuals[indi_id]
        for fam_id in individual.spouse:
            family = families[fam_id]
            if individual.birth != None and family.married != None:
                if individual.birth > family.married:
                    warnings.append(f'{individual.name} Married before birth')
    return warnings