from helpers import convert_date_to_string, check_and_convert_string_to_date
from datetime import date, datetime, timedelta
from collections import defaultdict
from typing import List

def US_29(individuals, families, tag_positions):
    warnings = []
    indi:List = []
    num1=[]
    for indi_id in individuals:
        individual = individuals[indi_id]
        if individual.alive == False and individual.death:
            num = tag_positions[individual.id]['NAME']
            warnings.append(  f'ANOMALY: INDIVIDUAL: US29: line {num} , The deceased individual is : {individual.name}')
    return warnings