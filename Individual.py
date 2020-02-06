#class for individual
class Individual: 
    def __init__(self, id):
        self.id = id
        self.name = None
        self.gender = None
        self.birthday = None
        self.age = None
        self.alive = True
        self.death = None
        self.child = {}
        self.spuse = {}