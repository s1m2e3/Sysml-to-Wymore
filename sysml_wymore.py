import xml.etree.ElementTree as ET
from system import *
tree = ET.parse('SIE558_Joanna Joseph_MA2.xml')
root = tree.getroot()
counter = 0
transitions = []


class states_node:
    def __init__(self):
        self.name = None
        self.child_nodes = []
        self.id = None
    
class transition:
    def __init__(self):
        
        self.id = None
        self.source = None
        self.target = None  

class activity:
    def __init__(self):
        
        self.id = None
        self.parent_state = None
        

# def build_transition_functions():

# def build_readout_functions():

def build_states(states,prev_name=""):
    
    state = states[0]

    if len(state.child_nodes)>1:
        prev_name = prev_name + state.name
        print("recursion in state")
        states.extend(build_states(state.child_nodes,prev_name))
        
        
    else:
        states.append(states_node())
        new_name = prev_name+state.name
        states[-1].name = new_name
        states[-1].id = state.id
        print("returned")        
    
        
    return states

# def clean_states(states):


# def build_inputs():

# def build_outputs():


def search(region,states,transitions,activities):
    for child in region:
        val = list(child.attrib)
        id_elem = [elem for elem in val if "id" in elem]
        source_elem = [elem for elem in val if "source" in elem]
        target_elem = [elem for elem in val if "target" in elem]
        val = [elem for elem in val if "type" in elem]
        
        if len(val)==1 and "uml:State" in child.attrib[val[0]] :
            print("found State")
            states.append(states_node())
            states[-1].name = child.attrib["name"]
            states[-1].id = child.attrib[id_elem[0]]
            print(states[-1].name,states[-1].id)
            print("checking if it has region")
            for sub_child in child:
                val = list(sub_child.attrib)
                
                val = [elem for elem in val if "type" in elem]

                if len(val)==1 and "uml:Region" in sub_child.attrib[val[0]] :
                    print("has region")
                    print("one recursion")
                    new_childs,_,_ = search(sub_child,states[-1].child_nodes,transitions,activities)
                    new_childs = [new_child for new_child in new_childs if type(new_child) == type(states[0])]
                    states[-1].child_nodes.extend(new_childs)
                    
                if len(val)==1 and "uml:Activity" in sub_child.attrib[val[0]] :
                    print("found activity")
                    activities.append(activity())
                    activities[-1].name = sub_child.attrib["name"]
                    activities[-1].parent_state = child.attrib[id_elem[0]]
        
        if len(val)==1 and "uml:Transition" in child.attrib[val[0]] :
            print("found Transition")
            transitions.append(transition())
            transitions[-1].id =child.attrib[id_elem[0]]
            transitions[-1].source =child.attrib[source_elem[0]]
            transitions[-1].target  =child.attrib[target_elem[0]]

    return states,transitions,activities

def structure_loop(structure):

    val = list(structure.attrib)
    val = [elem for elem in val if "type" in elem]
    
    if len(val)==1 and "uml:StateMachine" in structure.attrib[val[0]] :
        print("returning state machine ",structure.attrib['name'])
        return structure
            
    else: 
        for child in structure:
            val = list(child.attrib)
            val = [elem for elem in val if "type" in elem]
            if len(val)==1:
                if "uml:Package" in child.attrib[val[0]]:
                    structure = structure_loop(child)
                    val = list(structure.attrib)
                    val = [elem for elem in val if "type" in elem]

                    if len(val)==1 and "uml:StateMachine" in structure.attrib[val[0]] :
                        return structure

                    
                elif "uml:Class" in child.attrib[val[0]]:
                    structure = structure_loop(child)
                    val = list(structure.attrib)
                    val = [elem for elem in val if "type" in elem]
                    if len(val)==1 and "uml:StateMachine" in structure.attrib[val[0]] :
                        return structure
                    
                elif "uml:StateMachine" in child.attrib[val[0]]:
                    print("found state machine")
                    return child
                
                    
    return structure         
                
for child in root:
    if "Model" in child.tag:
        tag = child
        break
for child in tag:
    for element in child.attrib:
        if "Structure" in child.attrib[element]:
            print("found structure")
            structure = child
        if "Use Cases" in child.attrib[element]:
            print("found Use Cases")
            use_case = child

structure = structure_loop(structure)

for child in structure:
    for element in child.attrib:
        if "Region" in child.attrib[element]:
            print("found Region")
            region = child

states = []
transitions = []
activities = []

states,transitions,activities = search(region,states,transitions,activities)

states = build_states(states)


S = []
O = []
I = []
readout_ = {}
transition_ = {}
nodes = []


