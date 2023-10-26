class states_node:
    def __init__(self):
        self.name = None
        self.child_nodes = []
        self.id = None
        self.parent_id = None
        self.parent_region = None
        self.child_region = None
        self.orthogonal = False
        self.parallel = None

class pseudostate(states_node):
    def __init__(self):
        super().__init__()
        self.kind = None
        self.parent_region = None
        
class transition:
    def __init__(self):
        self.id = None
        self.source = None
        self.target = None  

class activity:
    def __init__(self):
        self.id = None
        self.name = None
        self.parent_id = None