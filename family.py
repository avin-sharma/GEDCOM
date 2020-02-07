class Family:
    def __init__(self, id):
        self.id = id
        self.married = None
        self.divorced = None
        # Husband
        self.hid = None 
        self.hname = None
        # Wife
        self.wid = None
        self.wname = None
        self.children = set()

        self.map = {
            'MARR': 'married',
            'HUSB' : 'hid',
            'WIFE': 'wid',
            'CHIL': self.children,
            'DIV': 'divorce'
        }
        