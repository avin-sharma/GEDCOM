def unique_name_and_birth(individuals):
    """This function will help to trace unique name and birthdate of the individuals"""
    z1 = []
    z3 = []
    warnings = []
    for indi_id in individuals:
        individual = individuals[indi_id]
        # print(type(individual.birth))
        z1.append(individual.name)
        z3.append(individual.birth)
    #print(z1)
    #print(z3)
    for i in range(len(z3) - 1):
        for j in range(i + 1, len(z3)):
            if z3[i] == z3[j]:
                #warnings.append(f"{z3[i]} has more than 1 name.")
                #war1.append(z3[i])
                if z1[i].split(" ")[0] == z1[j].split(" ")[0]:
                    if z1[i].split(" ")[1] == z1[j].split(" ")[1]:
                        warnings.append(f"{z1[i]} has similar name and birthdate.")
                        warnings.append(f"{z3[i]} has more than 1 name.")

    return warnings