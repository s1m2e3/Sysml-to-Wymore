import xml.etree.ElementTree as ET
from system import *
from itertools import product
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
        self.name = None
        self.parent_id = None
        


def build_states(states,prev_name=""):
    names = [state.name for state in states]
    states = states[0:len(names)]
    with_child = [states.index(state) for state in states if len(state.child_nodes)>1]
    without_child = [i for i in range(len(states)) if i not in with_child]
    
    for child_index in without_child:
        new_name = prev_name+states[child_index].name
        if new_name not in names:
            states.append(states_node())
            states[-1].name = new_name
            print(new_name)
            states[-1].id = states[child_index].id
                
    for child_index in with_child:
        new_name = prev_name + states[child_index].name
        appended,_ = build_states(states[child_index].child_nodes,new_name)
        states.extend(appended)
    
    return states,prev_name    
   

def search(region,states,transitions,activities):
    for child in region:
        val = list(child.attrib)
        id_elem = [elem for elem in val if "id" in elem]
        source_elem = [elem for elem in val if "source" in elem]
        target_elem = [elem for elem in val if "target" in elem]
        
        
        val = [elem for elem in val if "type" in elem]
        if len(val)==1 and "uml:State" in child.attrib[val[0]]:
            
            states.append(states_node())
            states[-1].name = child.attrib["name"]
            states[-1].id = child.attrib[id_elem[0]]
            
            
            for sub_child in child:
                val = list(sub_child.attrib)
                val = [elem for elem in val if "type" in elem]
                
                if len(val)==1 and "uml:Region" in sub_child.attrib[val[0]] :
                    
                    new_childs,_,_ = search(sub_child,states[-1].child_nodes,transitions,activities)
                    new_childs = [new_child for new_child in new_childs if type(new_child) == type(states[0])]
                    states[-1].child_nodes.extend(new_childs)
                if len(val)==1 and "uml:Activity" in sub_child.attrib[val[0]] :
                    
                    activities.append(activity())
                    activities[-1].name = sub_child.attrib["name"]
                    activities[-1].parent_id = child.attrib[id_elem[0]]
        
        if len(val)==1 and "uml:Transition" in child.attrib[val[0]] :
            
            transitions.append(transition())
            transitions[-1].id =child.attrib[id_elem[0]]
            transitions[-1].source =child.attrib[source_elem[0]]
            transitions[-1].target  =child.attrib[target_elem[0]]
      
    

    return states,transitions,activities

def structure_loop(structure):

    val = list(structure.attrib)
    val = [elem for elem in val if "type" in elem]
    
    if len(val)==1 and "uml:StateMachine" in structure.attrib[val[0]] :
        
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
                    
                    return child
                
                    
    return structure         

def clean_states(states):
    names = [state.name for state in states]
    counts = [i for i in range(len(names)) for j in range(len(names)) if names[i]==names[j] and i!=j]
    while len(counts)>0:
        del states[counts[0]]
        names = [state.name for state in states]
        counts = [i for i in range(len(names)) for j in range(len(names)) if names[i]==names[j] and i!=j]
    
    dropped_indices = []
    for i in range(len(names)):
        for j in range(len(names)):
            if names[i] in names[j] and i!=j:
                print(i,j)
                dropped_indices.append(i)
    dropped_indices=list(set(dropped_indices))          
    indices = [i for i in range(len(states)) if i not in dropped_indices]
    states = [states[i] for i in indices]
    
    return states

def find_state_machine_region(root):
    
    for child in root:
        if "Model" in child.tag:
            tag = child
            break
    model_name = tag.attrib["name"]

    for child in tag:
        for element in child.attrib:
            if "StateMachine" in child.attrib[element]:
                structure = child

            if "Structure" in child.attrib[element]:
                structure = child
            if "Class" in child.attrib[element]:
                class_ = child
                for subchild in class_:
                    for subelement in subchild.attrib:
                       if "StateMachine" in subchild.attrib[subelement]:
                            structure = subchild

                              
    structure = structure_loop(structure)
    regions = []
    for child in structure:
        for element in child.attrib:
            if "Region" in child.attrib[element]:
                regions.append(child)
            
    
    return regions,model_name

def build_system(states,transitions,activities):
    transition_pairs = []
    
    for transition in transitions:
        pair = (transition.source,transition.target)
        transition_pairs.append(pair)
    
    
    states,_ = build_states(states)
    states = clean_states(states)
    names = [state.name for state in states]
    ids = [state.id for state in states]

    named_transitions = []
    for pair in transition_pairs:
        if pair[0] in ids and pair[1] in ids:
            pair_ = (names[ids.index(pair[0])],names[ids.index(pair[1])])
            named_transitions.append(pair_)
    activities_parent_name = []
    activities_name = []
    
    for activity in activities:
        if activity.parent_id in ids:
            activities_name.append(activity.name)
            activities_parent_name.append(names[ids.index(activity.parent_id)])
            
    S = [State(state.name,[0,1]) for state in states]
    I = [Input("from_"+pair[0]+"to_"+pair[1],[0,1]) for pair in named_transitions]
    O = [Output(named_activity,[0,1]) for named_activity in activities_name]
    
    system = System(model_name,S,I,O)

    for i in range(len(I)):
        
        name = I[i].name
        prev_states_dictionary = {}
        next_states_dictionary = {}
        inputs_dictionary = {}
        for state in S:
            
            if "from_"+state.name in name:
                prev_states_dictionary[state.name]=1
            else:
                prev_states_dictionary[state.name]=0

            if "to_"+state.name in name:
                next_states_dictionary[state.name]=1
            else:
                next_states_dictionary[state.name]=0
        for input_ in I:
            if input_.name == name:
                inputs_dictionary[input_.name]=1
            else:
                inputs_dictionary[input_.name]=0
        prev = tuple(prev_states_dictionary.values())
        inpt =  tuple(inputs_dictionary.values())
        next = tuple(next_states_dictionary.values())
        # print(tuple(prev_states_dictionary.values()),tuple(next_states_dictionary.values()),tuple(inputs_dictionary.values()))
    #     func = lambda states_dict,inputs_dict: next_states_dictionary
    #     t = TransitionFunction(states_dict=prev_states_dictionary,inputs_dict=inputs_dictionary,function=func)
        
        system.addTransitionFunction(next,states= prev,inputs= inpt)
    #     print("added transition function")
    for o in range(len(O)):
        output_dictionary = {}
        states_dictionary = {}
        for j in range(len(O)):
            if o==j:
                output_dictionary[activities_name[j]] =1
            else:
                output_dictionary[activities_name[j]] =0
        state_index = names.index(activities_parent_name[o])
        for j in range(len(S)):
            if j == state_index:
                states_dictionary[names[j]] = 1
            else:
                states_dictionary[names[j]] = 0
        state = tuple(states_dictionary.values())
        output = tuple(output_dictionary.values())
        system.addReadoutFunction(output,state)
    
    return system

if __name__=="__main__":
    for fig in ['Fig1','Fig2','Fig3','Fig4','Fig5','Fig6']:
    # for fig in ["Fig2"]:
        print("\nTesting "+fig+"\n")
        tree = ET.parse(fig+'/com.nomagic.magicdraw.uml_model.model')
        root = tree.getroot()
        regions,model_name = find_state_machine_region(root)
        states = []
        transitions = []
        activities = []
        systems=[]
        
        for region in regions:
            states,transitions,activities = search(region,states,transitions,activities)
            system = build_system(states,transitions,activities)
            print([state.name for state in system.states])
            print([input_.name for input_ in system.inputs])
            
            print(system.readoutFunctions)
            print(system.transitionFunctions)
            systems.append(system)
        # if fig == "Fig1":
        #     system.setCurrentState((0,1))
        #     inputsVector=[(0,1),(1,0)]
        #     system.runExperiment(inputsVector)
        # elif fig == "Fig2":
        #     system.setCurrentState((0,1))
        #     inputsVector=[(0,1),(1,0)]
        #     system.runExperiment(inputsVector)    
        # print("\nstates found in system: \n")
        # for stateName in system.states:
        #     print(system.states[stateName].name,system.states[stateName].available_data)
        # print("\ninputs found in system: \n")
        # for inputName in system.inputs:
        #     print(system.inputs[inputName].name,system.inputs[inputName].available_data)
        # print("\noutputs found in system: \n")
        # for outputName in system.outputs:
        #     print(system.outputs[outputName].name,system.outputs[outputName].available_data)
        
        
        
        # # print(len(self.transition_functions)>=len(self.states)-1 and len(self.readout_functions)==len(self.all_states))
        # if system.validate_system():
        #     info_dict = {system.name:{}}
        #     inputTrajectories=[]
        #     if fig == "Fig1":
        #         inputTrajectories=[(1,0),(0,1)]
        #         initState = (1,0)
        #         info_dict[system.name]["inputs"]=inputTrajectories
        #         info_dict[system.name]["initial_state"]=initState
        #     elif fig == "Fig2":
        #         inputTrajectories=[(1,0),(0,1)]
        #         initState = (1,0)
        #     elif fig == "Fig3":
        #         inputTrajectories=[(1,0),(0,1)]
        #         initState = (1,0)
        #     elif fig == "Fig4":
        #         inputTrajectories=[(1,0),(0,1)]
        #         initState = (1,0)
        #     elif fig == "Fig5":
        #         inputTrajectories=[(1,0),(0,1)]
        #         initState = (1,0)
        #     elif fig == "Fig6":        
        #         inputTrajectories=[(1,0),(0,1)]
        #         initState = (1,0)
        #     system.run_experiment(len(inputTrajectories),info_dict)
        #     table = pd.DataFrame.from_dict(system.run_experiment(len(inputTrajectories),inputTrajectories,initState)).T
        #     table.columns = ["current_state","input","output"]
        #     print(table)
        # else:
        #     print("fail system "+ fig)

