from individual import Individual
from family import Family

from datetime import datetime
from prettytable import PrettyTable

from helpers import check_and_convert_string_to_date, convert_date_to_string
from collections import defaultdict

def save_information(inputs):
    """
    Takes input array and saves the information in data structures.

    inputs: array of tuples (level, tag, arguments)
    output: lists of individuals and families
    """
    # active here will hold either an individual or a family
    active_entity = None

    # to keep track of active tag at level 0 and 1. 2 only has a single tag DATE
    active_tags = {
        0: None,
        1: None
    }

    individuals = {}
    families = {}
    tag_positions = {}
    for num, level, tag, arguments in inputs:
        active_tags[level] = tag
        
        # Saving previous 0 level entity.
        if tag == 'INDI' or tag == 'FAM':
            if active_entity:
                if type(active_entity) is Individual:
                    individuals[active_entity.id] = active_entity
                else:
                    families[active_entity.id] = active_entity
            
            # assign active entity new individual or family based on the tag
            active_entity = Individual(arguments) if tag == 'INDI' else Family(arguments)
            # creating a new entity in tags dictionary so that we can add tags to it in the future
            tag_positions[arguments] = defaultdict(set)
            continue
            
        if level == 0:
            continue
        tag_positions[active_entity.id][tag].add(num)
        
        # Since all the three fields are sets we add elements to them.
        if tag in ['FAMC', 'FAMS', 'CHIL']:
            active_entity.map[tag].add(arguments)
        else:
            # If we have a date tag convert argument to datetime
            if level == 2:
                tag = active_tags[1]
                arguments = check_and_convert_string_to_date(arguments, num)

            setattr(active_entity, active_entity.map[tag], arguments)
    
    if type(active_entity) is Individual:
        individuals[active_entity.id] = active_entity
    else:
        families[active_entity.id] = active_entity
    
    # Update age for everyone, since its None in the beginning
    for id in individuals:
        current = individuals[id]
        current.name = ''.join(current.name.split('/'))
        
        deathday = None
        if current.birth:
            birthday = current.birth

            if current.death:
                deathday = current.death
                current.alive = False if deathday < datetime.now() else True
                if deathday > datetime.now():
                    deathday =  datetime.now()
            else:
                deathday =  datetime.now()
            difference = deathday - birthday
            current.age = (difference.days + difference.seconds//86400)//365
    
    # Update the husband and wife name for everyone, since its None in the beginning.
    for id in families:
        current = families[id]
        if current.hid:
            current.hname = individuals[current.hid].name
        
        if current.wid:
            current.wname = individuals[current.wid].name
    
    return individuals, families, tag_positions

def print_tables(data, type):
    table = PrettyTable()
    if type == 'INDI':
        table.field_names = ['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse']
        for key in sorted(data.keys()):
            current = data[key]
            table.add_row([current.id, 
            current.name if current.name else 'NA',
            current.gender if current.gender else 'NA',
            convert_date_to_string(current.birth) if current.birth else 'NA',
            current.age if current.age else 'NA',
            current.alive,
            convert_date_to_string(current.death) if current.death else 'NA',
            current.child if current.child else 'NA', 
            current.spouse if current.spouse else 'NA'])
    else:
        table.field_names = ['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children']
        for key in sorted(data.keys()):
            current = data[key]
            table.add_row([
                current.id,
                convert_date_to_string(current.married) if current.married else 'NA',
                convert_date_to_string(current.divorced) if current.divorced else 'NA',
                current.hid if current.hid else 'NA',
                current.hname if current.hname else 'NA',
                current.wid if current.wid else 'NA',
                current.wname if current.wname else 'NA',
                current.children if current.children else 'NA',
            ])
    return table