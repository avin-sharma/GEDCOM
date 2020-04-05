from datetime import datetime
from dateutil.relativedelta import relativedelta

def list_orphans(individuals, families, tag_positions):
    warning=[]
    present_date = datetime.now().date()
    for f_id in families:
        family=families[f_id]
        try:
            if family.hid !=None and family.wid!=None:
                if family.children!=set():
                    if individuals[family.hid].death!=None and individuals[family.wid].death!=None:
                        for i in family.children:
                            bdate=individuals[i].birth
                            try:
                                difference_in_years = relativedelta(present_date, bdate).years
                                if difference_in_years >=0 and difference_in_years<18:
                                    num=tag_positions[i]["NAME"]
                                    warning.append(f"ANOMALY: INDIVIDUAL: US33, line {num},is orphans.")
                            except:
                                continue
        except:
            continue
    return warning




def corresponding_entries(individuals,families,tag_positions):


    warning=[]

    for i_id in individuals:
        individual=individuals[i_id]
        try:

            if individual.child!=set():
                aa=list(individual.child)
                for f_id in families:
                    for i in range(len(aa)):
                        if aa[i] in f_id:
                            c=families[f_id].children
                            p=len(c)
                            if c==set():
                                num=tag_positions[i_id]["FAMC"]
                                warning.append(f"ANOMALY: US26,either line {num} does not have corresponding entry")

                            if p==1 :
                                if i_id not in c:
                                    num = tag_positions[aa[i]]['CHIL']
                                    #print(num)
                                    warning.append(f"ANOMALY: US26,either line {num} does not have corresponding entry")
                            if p>1:
                                if i_id not in list(c):
                                    #print("ii")
                                    num = tag_positions[aa[i]]["CHIL"]
                                    warning.append(f"ANOMALY: US26,either line {num} does not have corresponding entry")


        #For spouse

            if individual.spouse != set():
                aa1 = list(individual.spouse)
                for f_id in families:
                    for i in range(len(aa1)):
                        if aa1[i] in f_id:
                            c1 = families[f_id].hid
                            d=families[f_id].wid
                            if c1==None and d==None:
                                #print(c1)
                                #print(d)
                                #print(i_id)
                                num=tag_positions[i_id]["FAMS"]
                                #print("ppppp")
                                warning.append(f"ANOMALY: US26,either line {num} does not have corresponding entry")
                                continue
                            if i_id != c1:
                                if i_id != d:
                                    #print("vdge")
                                    num=tag_positions[i_id]["FAMS"]
                                    warning.append(f"ANOMALY: US26,either line {num} does not have corresponding entry")


        except:
            continue



    for f_id in families:
        try:

            if families[f_id].children!=set():
                m1=list(families[f_id].children)
                for i_id in individuals:
                    for i in range(len(m1)):
                        if m1[i] in i_id:
                            po=individuals[i_id].child
                            paa=len(po)
                            if po==set():
                                num=tag_positions[f_id]["CHIL"]
                                warning.append(f"ANOMALY: US26,either line {num} does not have corresponding entry")

                            if paa==1 :
                                if f_id not in po:
                                    #print("in keep it")
                                    num = tag_positions[m1[i]]["FAMC"]
                                    warning.append(f"ANOMALY: US26,either line {num} does not have corresponding entry")
                            if paa>1:
                                #print(list(po))
                                if f_id not in list(po):
                                    #print("dd")
                                    num = tag_positions[m1[i]]["FAMC"]
                                    warning.append(f"ANOMALY: US26,either line {num} does not have corresponding entry")

            if True:
                q1=families[f_id].hid
                q2=families[f_id].wid
                #print(q1,q2)
                for i_id in individuals:
                    if q1 in i_id:
                        k1=individuals[i_id].spouse
                        l1=len(k1)
                        #print(k1)
                        if l1==0:
                            if f_id not in k1:
                                #print("i")
                                num=tag_positions[f_id]["HUSB"]
                                #print("w1")
                                warning.append(f"ANOMALY: US26,either line {num} does not have corresponding entry")
                        if l1==1:
                            if f_id not in k1:
                                num=tag_positions[i_id]["FAMS"]
                                #print("w2")
                                warning.append(f"ANOMALY: US26,either line {num} does not have corresponding entry")
                        if l1>1:
                            if f_id not in list(k1):
                                #print("W3")
                                num=tag_positions[q1]["FAMS"]
                                warning.append(f"ANOMALY: US26,either line {num} does not have corresponding entry")

                    if q2 in i_id:
                        #print(q2)
                        k2=individuals[i_id].spouse
                        l2=len(k2)
                        if l2==0:
                            if f_id not in k2:
                                #print("ooo")
                                num=tag_positions[f_id]["WIFE"]
                                warning.append(f"ANOMALY: US26,either line {num} does not have corresponding entry")
                        if l2==1:
                            if f_id not in k2:
                                #print(" fve")
                                num=tag_positions[i_id]["FAMS"]
                                warning.append(f"ANOMALY: US26,either line {num} does not have corresponding entry")
                        if l2>1:
                            if f_id not in list(k2):
                                #print("qcqcv")
                                num=tag_positions[q2]["HUSB"]
                                warning.append(f"ANOMALY: US26,either line {num} does not have corresponding entry")

        except:
            continue


    return list(set(warning))