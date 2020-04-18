from datetime import datetime
import prettytable

def listLivingMarried(individuals, families, tag_positions):
    warnings = []
    ftable = prettytable.PrettyTable()
    ftable.field_names = ["Individual Name", "Line"]
    for indi_id in individuals:
        individual = individuals[indi_id]
        if(individual.alive == True and individual.spouse != None):
            num = tag_positions[indi_id]['NAME']
            ftable.add_row([individual.name,num])
    warnings.append(
                f'INDIVIDUAL: US30,Above Table shows individuals who are married and alive')
    print(f"{str(ftable)}\n")
    return warnings
    # warnings = []
    # for indi_id in individuals:
    #     individual = individuals[indi_id]
    #     if(individual.alive == True and individual.spouse != None):
    #         num = tag_positions[indi_id]['NAME']
    #         warnings.append(
    #             f'INDIVIDUAL: US30, Line {num} {individual.name} is married and alive')
    # return warnings


def includeindividualage(individuals, families, tag_positions):
    warnings = []
    ftable = prettytable.PrettyTable()
    ftable.field_names = ["Individual Name","Age","Line"]
    for indi_id in individuals:
        individual = individuals[indi_id]
        if(individual.alive == True and individual.age != None):
            num = tag_positions[indi_id]['NAME']
            ftable.add_row([individual.name,individual.age,num])
    warnings.append(
                f'INDIVIDUAL: US27,Above Table shows individuals with their age')
    print(f"{str(ftable)}\n")
    return warnings
    # warnings = []
    # for indi_id in individuals:
    #     individual = individuals[indi_id]
    #     if(individual.alive == True and individual.age != None):
    #         num = tag_positions[indi_id]['NAME']
    #         warnings.append(
    #             f'INDIVIDUAL: US27, Line {num} {individual.name} is {individual.age} years old in the GEDCOM file')
    # return warnings


    