class Individual:
    def __init__(self, id):
        self.id = id
        self.name = None
        self.gender = None
        self.birth = None
        self.age = None
        self.alive = True
        self.death = None
        self.child = set()
        self.spouse = set()

        self.map = {
            'NAME': 'name',
            'SEX' : 'gender',
            'BIRT': 'birth',
            'DEAT': 'death',
            'FAMC': self.child,
            'FAMS': self.spouse
        }
    
    def __repr__(self):
        return f"Name: {self.name}, Sex: {self.gender}, Birth: {self.birth}, Death: {self.death}, Age: {self.age}, Child: {self.child}, Spouse: {self.spouse} \n"