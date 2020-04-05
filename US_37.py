from helpers import convert_date_to_string, check_and_convert_string_to_date
from datetime import date, datetime, timedelta

def US_37(individuals, families, tag_positions):
    warnings = []
    for fam_id, family in families.items():
        if family.hid != None and family.wid != None:
            hdetail = individuals[family.hid]
            wdetail = individuals[family.wid]
            if hdetail.spouse.intersection(wdetail.spouse) or wdetail.spouse.intersection(hdetail.spouse):
                if hdetail.death != None:
                    d1 = (hdetail.death.date())
                    d2 = (datetime.now().date())
                    if (d2 - d1).days < 30:
                        #if wdetail.death != None:
                        for key, value in individuals.items():
                            if family.children == {key}:
                                if wdetail.death == None:
                                    num3 = tag_positions[family.wid]['NAME']
                                    num4 = tag_positions[individuals[value.id].id]['NAME']
                                    warnings.append(f'ANOMALY: FAMILY: US37: line {num3} and {num4}, Living Spouse: {wdetail.name} and Descendant: {value.name} .')

                if wdetail.death != None:
                    d3 = (wdetail.death.date())
                    d4 = (datetime.now().date())
                    if (d4 - d3).days < 30:
                        for key, value in individuals.items():
                            if family.children == {key}:
                                if hdetail.death == None:
                                    num1 = tag_positions[family.hid]['NAME']
                                    num2 = tag_positions[individuals[value.id].id]['NAME']
                                    warnings.append(f'ANOMALY: FAMILY: US37: line {num1} and {num2}, Living Spouse: {hdetail.name} and Descendant: {value.name} .')

    return warnings