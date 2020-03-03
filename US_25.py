from helpers import convert_date_to_string
def US_25(individuals, families):
    warnings=[]
    for family in families.values():
        names = set()
        birth_dates = set()

        for child_id in family.children:
            child = individuals[child_id]
            if child.name in names:
                warnings.append(child.name)
                # Do something here
            if child.birth in birth_dates:
                child.birth=convert_date_to_string(child.birth)
                warnings.append(child.birth)
            birth_dates.add(child.birth)
            names.add(child.name)
    return warnings