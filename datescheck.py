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

def check_BirthBeforeDeath(individuals,tag_positions): ##US03 : Birth should occur before death of an individual
    warnings = []
    for indi_id in individuals:
        individual = individuals[indi_id]
        if individual.death != None and individual.birth != None:
            if individual.birth > individual.death:
                num = tag_positions[indi_id]['DEAT']|tag_positions[indi_id]['BIRT']
                warnings.append(f'ANOMALY: Individual: US03, line {num},{individual.name} died before birth')
    return warnings

def check_BirthBeforeMarriageOfParents(individuals,families, tag_positions): ##US08: Birth before marriage of parents
    warnings = []
    for fam_id in families:
        family = families[fam_id]
        for child_id in family.children:
            individual = individuals[child_id]
            if individual.birth != None and family.married != None:
                if(individual.birth < family.married):
                    num = tag_positions[child_id]['BIRT']
                    warnings.append(f'ANOMALY: FAMILY: US08, line {num},{individual.name} was born before marriage of parents')
    return warnings
    
def check_BirthAfterDivorceOfParents(individuals,families, tag_positions):##US 08 born not more than 9 months after their divorce
    warnings = []
    for fam_id in families:
        family = families[fam_id]
        for child_id in family.children:
            individual = individuals[child_id]
            if individual.birth != None and family.married != None:
                if individual.birth != None and family.divorced != None:
                    divorceDayDifference = family.divorced - individual.birth
                    if(divorceDayDifference.days < -275):
                        num = tag_positions[child_id]['BIRT']
                        warnings.append(f'ANOMALY: FAMILY: US08, line {num},{individual.name} born more than 9 months after divorce of parents')
    return warnings
# US09	Birth before death of parents	Child should be born before death of mother and before 9 months after death of father

def check_BirthBeforeDeathOfMother(individuals,families, tag_positions):
    warnings = []
    for fam_id in families:
        family = families[fam_id]
        for child_id in family.children:
            if family.wid != None:
                individual_child = individuals[child_id]
                individual_mother = individuals[family.wid]
                if individual_child.birth != None and  individual_mother.death != None:
                    if individual_child.birth > individual_mother.death:
                        num = tag_positions[child_id]['BIRT']
                        warnings.append(f'ANOMALY: FAMILY: US09, line{num},{individual_child.name} born after death of mother {individual_mother.name}')
    return warnings

def check_BirthAfterDeathOfFather(individuals,families, tag_positions):
    warnings = []
    for fam_id in families:
        family = families[fam_id]
        for child_id in family.children:
            if family.hid != None:
                individual_father = individuals[family.hid]
                individual_child = individuals[child_id]
                if individual_child.birth != None and  individual_father.death != None:
                    diff = individual_father.death - individual_child.birth
                    if diff.days < -275:
                        num = tag_positions[child_id]['BIRT']
                        warnings.append(f'ANOMALY: FAMILY: US09, line{num},{individual_child.name} born 9 months after death of father {individual_father.name}')
    return warnings

# US10	Marriage after 14	Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old)

def check_BirthofParents(individuals,families, tag_positions):
    warnings = []
    for fam_id in families:
        family = families[fam_id]
        if family.hid != None:
            individual_father = individuals[family.hid]
        if family.wid != None:
            individual_mother = individuals[family.wid]
            for child_id in family.children:
                individual_child = individuals[child_id]
                if individual_father.age != None and individual_father.age < 14:
                    num = tag_positions[family.hid]['BIRT']
                    warnings.append(f'ANOMALY: FAMILY: US10, line{num}, {individual_father.name} Father of child {individual_child.name} is less than 14 years old')
                if individual_mother.age != None and individual_mother.age < 14:
                    num = tag_positions[family.wid]['BIRT']
                    warnings.append(f'ANOMALY: FAMILY: US10, line{num}, {individual_mother.name} Mother of child {individual_child.name} is less than 14 years old')
    return warnings

#US12 Parents not too old Mother should be less than 60 years older than her children and father should be less than 80 years older than his children

def check_ParentsNotTooOld(individuals,families, tag_positions):
    warnings = []
    for fam_id in families:
        family = families[fam_id]
        if family.hid != None:
            individual_father = individuals[family.hid]
        if family.wid != None:
            individual_mother = individuals[family.wid]
            for child_id in family.children:
                individual_child = individuals[child_id]
                if individual_father.age != None and individual_child.age != None:
                    diff = individual_father.age - individual_child.age
                    if(diff >= 80):
                        num = tag_positions[family.hid]['BIRT']
                        warnings.append(f'ANOMALY: FAMILY: US12, line{num}, {individual_father.name} Father of child {individual_child.name} is elder by 80 or more years')
                if individual_mother.age != None and individual_child.age != None:
                    diff = individual_mother.age - individual_child.age
                    if(diff >= 60):
                        num = tag_positions[family.wid]['BIRT']
                        warnings.append(f'ANOMALY: FAMILY: US12, line{num}, {individual_mother.name} Mother of child {individual_child.name} is elder by 60 or more years')        
    return warnings

#US14 Multiple births <= 5 No more than five siblings should be born at the same time
def check_MultipleBirths(individuals,families, tag_positions):
    warnings = []
    dob = {}
    for fam_id in families:
        family = families[fam_id]
        if len(family.children) > 5:
            for child_id in family.children:
                individual_child = individuals[child_id]
                if individual_child.birth != None:
                    dob[individual_child.birth] = dob.get(individual_child.birth, 0) + 1
            for val in dob.values():
                if val > 5:
                    warnings.append(f'ANOMALY: FAMILY: US14 {fam_id} has more than 5 siblings born on same time')
                    break
    return warnings