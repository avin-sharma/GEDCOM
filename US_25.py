from collections import Counter
def US_25(individuals,families):
    #warning=set()
    f={}
    a={}
    b={}
    z={}
    counter=0
    for family in families.values():
        a=family.id
        if a == family.id:
            a=family.children
            #print(a)
            for indi_id in individuals:
                individual=individuals[indi_id]
                f={indi_id}
                z={family.id}
                if f & a ==f:
                    if z == individual.child:
                        print(individual.name)
                        print(individual.birth)
                        if individual.name and individual.birth:
                            counter+=1
                            if counter>1:
                                print("Same name and birthdate occured")
                    #if individual.child & a ==individual.child:
                     #   print(individual.name)
                      #  print(individual.birth)
