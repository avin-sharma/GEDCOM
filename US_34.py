def US_34(individuals, families, tag_positions):
    warnings = []
    y3 = []
    y4 = []
    for fam_id, family in families.items():
        if family.hid != None and family.wid != None:
            num = tag_positions[family.hid]['NAME']
            num1 = tag_positions[family.wid]['NAME']
            hdetail = individuals[family.hid]
            wdetail = individuals[family.wid]
            hage = hdetail.age
            wage = wdetail.age
            if hage != None and wage != None:
                y3.append(hage)
                y4.append(wage)
                agediff = hage / wage
                if agediff > 2 or agediff < 0.5:
                    warnings.append(f'ANOMALY: FAMILY: US34: line {num} and {num1}, {family.hname} and {family.wname} are the couples who were married when the older spouse was more than twice as old as the younger spouse.')

    return warnings