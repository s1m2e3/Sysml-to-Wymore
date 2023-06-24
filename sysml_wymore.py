import xml.etree.ElementTree as ET
from system import *
tree = ET.parse('SIE558_Joanna Joseph_MA2.xml')
root = tree.getroot()
counter = 0
transitions = []
states = {}

def search(region,states):
    for child in region:
        val = list(child.attrib)
        val = [elem for elem in val if "type" in elem ][0]
        if "uml:State" in child.attrib[val]:
            print("checking if has region")
            for sub_child in child:
                val = list(child.attrib)
                val = [elem for elem in val if "type" in elem ][0]
                if "uml:Region" in sub_child.attrib[val]:
                    print("has region")
                    states = search(sub_child,states)
            print("none had region, terminal nodes")

    return states

def structure_loop(structure):
    for child in structure:
        val = list(child.attrib)
        val = [elem for elem in val if "type" in elem]

        if len(val)==1:
            
            if "uml:Package" in child.attrib[val[0]]:
                
                structure = structure_loop(child)
            elif "uml:Class" in child.attrib[val[0]]:
                
                structure = structure_loop(child)
            elif "uml:StateMachine" in child.attrib[val[0]]:
                
                break
                
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
ssm = structure
# for child in structure:
    # for element in child.attrib:
        # print(child.attrib[element])
        # if "State Machine" in child.attrib[element]:
            # print("found System State Machine")
            # ssm = child
 
for child in ssm:
    for element in child.attrib:
        if "Region" in child.attrib[element]:
            print("found Region")
            region = child

states = search(region,states)

for child in region: 
    # keys = list(.attrib)
    # val = list(child.attrib)
    # val = [elem for elem in val if "type" in elem ][0]
    # print(type(child.attrib[val]))
    for element in child.attrib:
        
        if "State" in child.attrib[element]:
            states.append(child)
        if "Transition" in child.attrib[element]:

            print("found Transitions")
            transitions.append(child)
S = []
O = []
I = []
readout_ = {}
transition_ = {}
nodes = []

for state in states:
    for element in state.attrib:
        if element == "name":
            name_state = state.attrib[element]
        if "id" in element:
            nodes.append(state.attrib[element])
    for child in state:
        if "Activity" in child.tag:
            for element in child.attrib:
                if element == "name":
                    name_output = child.attrib[element]
                    output_type = "II"
                    data = [0,1]
                    O.append(Output(name=name_output,output_type=output_type,data=data))
                    readout_[name_state+"_"+name_output]=1
    state_type="II"
    data=[0,1]
    S.append(State(name_state,state_type=state_type,data=data))

for transition in transitions:
    print(transition.tag,transition.attrib)
    # for element in transition.attrib:
        # print(element)
        # if "name" == element:
        #     name_input = transition.attrib[element]
        #     transition_[name_input]={}
        # elif "source" == element:
        #     transition_[name_input]["source"]=transition.attrib[element]
        # elif "target" == element:
        #     transition_[name_input]["target"]=transition.attrib[element]
    
    # input_type = "II"
    # data=[0,1]
    # I.append(Input(name_input,input_type=input_type,data=data))
        
       