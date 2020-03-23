from collections import defaultdict
from datetime import datetime
def recent_births(individuals, tag_positions):
    x1=[]
    x2=[]
    x3=[]
    warnings=[]
    for indi_id in individuals:
        individual = individuals[indi_id]
        try:
            x1.append(individual.birth.date())
            x2.append(indi_id)
            x3.append(individual.name)
        except:
            x1.append(individual.birth)
            x2.append(indi_id)
            x3.append(individual.name)
    present_date=datetime.now().date()
    for i in range(len(x1)):
        try:
            if abs((x1[i]-present_date).days)<=30:
                num = tag_positions[x2[i]]['NAME']
                warnings.append(f"ANOMALY: INDIVIDUAL: US35, line {num}, {x3[i]} has most recent birthday.")
        except:
            continue
    #print(warnings)
    return warnings

def recent_deaths(individuals, tag_positions):
    x1=[]
    x2=[]
    x3=[]
    warnings=[]
    for indi_id in individuals:
        individual = individuals[indi_id]
        try:
            x1.append(individual.death.date())
            x2.append(indi_id)
            x3.append(individual.name)
        except:
            x1.append(individual.death)
            x2.append(indi_id)
            x3.append(individual.name)
    present_date = datetime.now().date()

    for j in range(len(x1)):
        try:
            if abs((x1[j]-present_date).days)<=30:
                num = tag_positions[x2[j]]['NAME']
                warnings.append(f"ANOMALY: INDIVIDUAL: US36, line {num}, {x3[j]} has most recent death.")
        except:
            continue
    #print(warnings)
    return warnings