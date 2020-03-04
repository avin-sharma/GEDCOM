from datetime import datetime

def bigamy(individuals, families, tag_positions):
    """ 
    User Story 11
    Marriage should not occur during marriage to another spouse.
    
    returns: a list of warning strings.
    """
    warnings = []
    # Find of someone is married once
    # Then check if they dont have any other active marriage(married before today).
    # Ignore active marriages with dead(death before today) spouses.
    
    for indi_id in individuals:
        individual = individuals[indi_id]
        count = 0

        if individual.spouse:
            for fam_id in individual.spouse:
                if is_married(individuals, families, fam_id):
                    count += 1

        if count > 1:
            num = tag_positions[indi_id]['FAMS']
            warnings.append(f'ANOMALY: INDIVIDUAL: US11, line {num}, {individual.name} has more than 1 active marriages!')
    
    return warnings

def is_married(individuals, families, family_id):
    """
    Checks if the spouses of a given family are presently married.

    They are not married if divorce date is present and is before today
    and if one of the spouses is not alive.

    returns: a boolean
    """
    family = families[family_id]
    divorce_date = family.divorced
    if divorce_date and divorce_date < datetime.now():
        return False
    
    if not family.hid or not family.wid:
        return False
    
    # if one of the partners has passed away, they are not married.
    if not is_alive(individuals, family.hid) or not is_alive(individuals, family.wid):
        return False

    return True

def is_alive(individuals, individual_id):
    """
    Checks if the individual with the given id is alive.
    """
    return individuals[individual_id].alive

def first_cousins_married(individuals, families, tag_positions):
    """
    User Story 19

    Searches and warns if first cousins are married
    in the given families and individuals.

    returns: a list of warning strings
    """
    warnings = []

    for fam_id in families:
        family = families[fam_id]
        parents_child_at = set()

        if not family.hid or not family.wid:
            continue

        husband = individuals[family.hid]
        wife = individuals[family.wid]

        h_parents = get_parents(individuals, families, family.hid)
        w_parents = get_parents(individuals, families, family.wid)

        # add parents family where they are child to the variable
        h_parents_famc = get_parents_famc(individuals, families, family.hid)
        w_parents_famc = get_parents_famc(individuals, families, family.wid)

        if h_parents_famc.intersection(w_parents_famc) and not h_parents.intersection(w_parents):
            num = tag_positions[fam_id]['HUSB'] | tag_positions[fam_id]['WIFE'] | tag_positions[family.hid]['FAMS'] | tag_positions[family.wid]['FAMS']
            warnings.append(f'ANOMALY: FAMILY: US19, line {num} {husband.name} is married to his first cousin {wife.name}!')
    
    return warnings
        

def get_parents_famc(individuals, families, indi_id):
    """
    Find family id of both the parents of the given person.
    """
    if not indi_id:
        return set()
        
    individual = individuals[indi_id]
    parents_famc = set()

    
    if not individual.child:
        return set()
    
    for famc in individual.child:
        family = families[famc]
        father = individuals[family.hid]
        mother = individuals[family.wid]

        if father.child:
            parents_famc.update(father.child)
        if mother.child:
            parents_famc.update(mother.child)
    
    return parents_famc

def get_parents(individuals, families, indi_id):
    """
    Find parents of the given person.
    """
    if not indi_id:
        return set()
        
    individual = individuals[indi_id]
    parents = set()
    
    if not individual.child:
        return set()
    
    for famc in individual.child:
        family = families[famc]
        father = individuals[family.hid]
        mother = individuals[family.wid]

        if father:
            parents.add(father)
        if mother:
            parents.add(mother)
    
    return parents

def check_sibling_counts(individuals, families, tag_positions):
    """
    User Story 15

    There should be fewer than 15 siblings in a family.

    returns: a list of warning strings.
    """
    warnings = []
    for fam_id in families:
        family = families[fam_id]

        if family.children and len(family.children) >= 15:
            num = tag_positions[fam_id]['CHIL']
            for child_id in family.children:
                num.update(tag_positions[child_id]['FAMC'])
            warnings.append(f'ANOMALY: FAMILY: US15, line {sorted(num)} Family {fam_id} has more than 14 siblings!')
    
    return warnings