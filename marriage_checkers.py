from datetime import datetime

def bigamy(individuals, families):
    """ 
    User Story 11
    Marriage should not occur during marriage to another spouse.
    
    """

    # Find of someone is married once
    # Then check if they dont have any other active marriage(married before today).
    # Ignore active marriages with dead(death before today) spouses.
    for indi_id in individuals:
        individual = individuals[indi_id]
        count = 0
        for fam_id in individual.spouse:
            if is_married(individuals, families, fam_id):
                count += 1
        
        if count > 1:
            return f'{individual.name} has more than 1 active marriages!'

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
    
    # if one of the partners has passed away, they are not married.
    if not is_alive(individuals, family.hid) or not is_alive(individuals, family.wid):
        return False

    return True

def is_alive(individuals, individual_id):
    """
    check if the individual with the given id is alive.
    """
    return individuals[individual_id].alive
