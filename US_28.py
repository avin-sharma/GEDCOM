from helpers import convert_date_to_string, check_and_convert_string_to_date
from datetime import date, datetime, timedelta
from typing import DefaultDict,List
from collections import defaultdict,OrderedDict
import operator


def US_28(individuals, families, tag_positions):
    warnings = []
    siblings: DefaultDict = defaultdict(list)
    siblings1: DefaultDict = defaultdict(list)
    age:DefaultDict = defaultdict(list)
    num1:DefaultDict = defaultdict(list)
    ua:list = []
    numline:list=[]
    sortbirth:list = []

    for fam_id in families:
        family = families[fam_id]
        currentsiblings = family.children
        for indi_id in individuals:
            individual = individuals[indi_id]
            if len(family.children) > 1:
                if individual.id in family.children:
                    for a in currentsiblings:
                        if a == individual.id:
                            child = individuals[individual.id]
                            if child.name not in siblings.values():
                                if child.birth is not None:
                                    siblings[str(child.child)].append(child.birth)
                                    age[str(child.child)].append(child.name)
                                    siblings1[str(child.child)].append(age)
                                    num = tag_positions[individual.id]['NAME']
                                    num1[str(child.child)].append(num)
    #for key,value in siblings1.items():
    for key, value in sorted(siblings.items(), key=operator.itemgetter(1)):
        for k, v in age.items():
            if key == k:
                ua.append(v)
        for n in num1.keys():
            if key == n:
                numline.append(num1[n])
        warnings.append(
                   f'ANOMALY: FAMILY: US28: line {numline} , The list of sibling in Family with Family ID {key} is {ua}')
        #print(siblings1)
        ua=[]
        numline=[]
        birth=[]
    return warnings

