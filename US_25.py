from helpers import convert_date_to_string
from collections import defaultdict
def US_25(individuals, families, tag_positions):
    warnings=[]
    for family in families.values():
        names = set()
        birth_dates = defaultdict(set)

        for child_id in family.children:
            child = individuals[child_id]
            if child.name in names:
                num = tag_positions[child_id]['NAME']
                warnings.append(f'ANOMALY: US25: line {num}, There are multiple {child.name} in the family.')
            
            num = tag_positions[child_id]['BIRT']
            if child.birth in birth_dates:
                birthdate = convert_date_to_string(child.birth)
                warnings.append(f'ANOMALY: US25: line {birth_dates[child.birth] | num}, There are multiple people born on {birthdate} in the family.')
                
            birth_dates[child.birth] |= num
            names.add(child.name)
    return warnings