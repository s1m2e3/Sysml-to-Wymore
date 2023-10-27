from sysml_subclasses import *
from system import *
import numpy as np
import xml.etree.ElementTree as ET
from itertools import product
import copy

def find_child(root,tagName=None,attribName=None,exhaustive=False):
    if tagName is not None:
        tag = None
        for child in root:
            if tagName in child.tag:
                tag = child
                break
        return tag

    if attribName is not None and not exhaustive:
        tag = None 
        for child in root:
            for element in child.attrib:
                
                if attribName in child.attrib[element]:
                    tag = child
                    break
        return tag
    elif attribName is not None and exhaustive:
        tag = [] 
        for child in root:
            for element in child.attrib:
                
                if attribName in child.attrib[element]:
                    tag.append(child)
        return tag
def attrib_in_root(root,attribName=None):
    if attribName is not None:
        for element in root.attrib:
                if attribName in root.attrib[element]:
                    return True
        return False
def get_attrib_in_root(root,attribName=None):
    if attribName is not None:
        for element in root.attrib:
            if attribName in element:
                return root.attrib[element]
def structure_loop(structure):
    
    attribName = "uml:StateMachine"
    if attrib_in_root(structure,attribName):
        return structure 
            
    else: 
        for attribName in ["uml:Package","uml:Class"]:
            structure = find_child(structure,attribName=attribName)
            if attrib_in_root(structure,"uml:StateMachine"):
                return structure 
def find_state_machine_region(root):
    
    tag = find_child(root,tagName="Model")
    model_name = tag.attrib["name"]
    
    for attribName in ["StateMachine","Structure"]:
        structure = find_child(tag,attribName = attribName)
        if structure is not None:
            break
    
    if structure is None:
        attribName = "Class"
        structure = find_child(tag,attribName = attribName)
        
        if structure is not None:
            structure = find_child(structure,attribName = "uml:StateMachine")
            
        else:
            ValueError("state machine not in statemachine, class or structure tags")
    
                      
    structure = structure_loop(structure)
    regions = []
    
    for child in structure:
        for element in child.attrib:
            if "Region" in child.attrib[element]:
                regions.append(child)
            
    
    return regions,model_name
def generatePseudostate(pseudostates,pseudoChild):
    pseudostates.append(pseudostate())
    if attrib_in_root(pseudoChild,attribName="kind"):
        pseudostates[-1].kind = get_attrib_in_root(pseudoChild,attribName="kind")
    pseudostates[-1].id = get_attrib_in_root(pseudoChild,attribName="id")
    return pseudostates
def generateTransition(transitions,transitionChild):
    transitions.append(transition())
    transitions[-1].id = get_attrib_in_root(transitionChild,attribName="id")
    transitions[-1].source = get_attrib_in_root(transitionChild,attribName="source")
    transitions[-1].target  = get_attrib_in_root(transitionChild,attribName="target")
    return transitions
def generateActivity(activities,activityChild):
    activities.append(activity())
    activities[-1].name = get_attrib_in_root(activityChild,attribName="name")
    return activities
def generateState(states,stateChild):
    states.append(states_node())
    states[-1].name = get_attrib_in_root(stateChild,attribName="name")
    states[-1].id = get_attrib_in_root(stateChild,attribName="id")
    regionName = "uml:Region"
    subRegion = find_child(stateChild,attribName=regionName,exhaustive=True)
    if subRegion is not None:
        states[-1].child_region = subRegion
     
    return states
def search(region,pseudostates,states,transitions,activities):
    pseudoAttrib = "uml:Pseudostate"
    transitionAttrib = "uml:Transition"
    stateAttrib = "uml:State"
    activityAttrib = "uml:Activity"
    pseudoChildren= find_child(region,attribName=pseudoAttrib,exhaustive=True)
    transitionChildren = find_child(region,attribName=transitionAttrib,exhaustive=True)
    stateChildren = find_child(region,attribName=stateAttrib,exhaustive=True)
    if pseudoChildren is not None:
        for pseudoChild in pseudoChildren:
                pseudostates = generatePseudostate(pseudostates,pseudoChild)
                pseudostates[-1].parent_region = region        
    if transitionChildren is not None:
        for transitionChild in transitionChildren:
            transitions = generateTransition(transitions,transitionChild)
    if stateChildren is not None:
        for stateChild in stateChildren:
            states = generateState(states,stateChild)
            states[-1].parent_region = region
            stateTransitionChildren = find_child(stateChild,attribName=transitionAttrib,exhaustive=True)
            stateActivityChildren = find_child(stateChild,attribName=activityAttrib,exhaustive=True)
            if stateTransitionChildren is not None:
                for stateTransitionChild in stateTransitionChildren:
                    transitions = generateTransition(transitions,stateTransitionChild)
            if stateActivityChildren is not None:
                for stateActivityChild in stateActivityChildren:
                    activities = generateActivity(activities,stateActivityChild)
                    activities[-1].parent_id = states[-1].id
                    
            if states[-1].child_region is not None: 
                if len(states[-1].child_region)>0:
                    for subRegion in states[-1].child_region:
                        
                        pseudostates,newStateChildren,_,_= search(subRegion,pseudostates,states[-1].child_nodes,transitions,activities)
                        newStateChildren = [newStateChild for newStateChild in newStateChildren if type(newStateChild) == type(states[0])]
                        states[-1].child_nodes.extend(newStateChildren)
                        
                # else:
                #     subRegion = states[-1].child_region
                #     print(states[-1].name)
                #     input("hey,in subregion")
                #     pseudostates,newStateChildren,_,_= search(subRegion,pseudostates,states[-1].child_nodes,transitions,activities)
                #     print([newStateChild for newStateChild in newStateChildren if type(newStateChild) == type(states[0])])
                #     print(newStateChildren,states[0])
                #     input("hey,in subregion compairson")
                #     newStateChildren = [newStateChild for newStateChild in newStateChildren if type(newStateChild) == type(states[0])]
                #     states[-1].child_nodes.extend(newStateChildren)
                #     print(states[-1].name,states[-1].child_nodes)
    
    return pseudostates,states,transitions,activities
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
            states[-1].id = states[child_index].id
    for child_index in with_child:
        new_name = prev_name + states[child_index].name
        appended,_ = build_states(states[child_index].child_nodes,new_name)
        states.extend(appended)
    return states,prev_name    
def findParallel(states):
    parallelNames = []
    parentRegions = [state.parent_region for state in states] 
    childRegions = [state.child_region for state in states]
    for childRegion in childRegions:
        if childRegion is not None and type(childRegion)==type([]):
            if len(childRegion)>1:
                for region in childRegion:
                    childStateIndex = list(set([states[i].name for i in range(len(parentRegions)) if parentRegions[i] == region]))
                    parallelNames.append(childStateIndex)
    return parallelNames
def setParallel(states,parallel_names):
    names = [state.name for state in states]
    for state in states:
        for cluster in parallel_names:
            if state.name in cluster:
                state.parallel = [name for name in cluster if name != state.name]
    return states
def getpossibleParents(states):
    possibleParents = [state for state in states if state.parent_id is not None and state.parent_region is not None and state.child_region is not None]
    return possibleParents
def getParents(states):
    parents = [state for state in states if state.parent_id is not None  and state.child_region is not None and len(state.child_region)>0]
    return parents
def getChildRegions(states):
    state_regions_child = [state.child_region for state in states if state.child_region is not None and len(state.child_region)>0]
    return state_regions_child
def getChildRegionsExtended(states):
    state_regions_child = [state for state in states if state.child_region is not None and len(state.child_region)>0]
    stateRegionsChild = []
    stateRegionsChildIndexes = []
    for state in state_regions_child:
        stateRegionsChild.extend(state.child_region)
        stateRegionsChildIndexes.append(states.index(state))
    return stateRegionsChild,stateRegionsChildIndexes
def findSetParent(states):
    parents_and_childs_states = [state for state in states if state.parent_region is not None and state.child_region is not None]
    regionChildStates = [state for state in states if state.child_region is not None if len(state.child_region)>0]
    for state in regionChildStates:
        for state_ in states:
            if state!=state_ and  state_.parent_region in state.child_region:
                state_.parent_id = state.id

    possibleParents = getpossibleParents(states)
    for state in states:
        compatibility = [parent for parent in possibleParents if state.parent_region in parent.child_region]
        for parent in compatibility:
            state.parent_id = [parent.id]
            state.parent_id.append(parent.parent_id)
    parents = getParents(states)
    parentsName = [state.name for state in parents]     
    
    for state in states:
        compatibility = [parent for parent in parents if parent.name in state.name and parent.name != state.name]
        if len(compatibility)>0:
            state.parent_id = list(np.unique(np.array([parent.parent_id for parent in compatibility])))
    return states
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
                dropped_indices.append(i)
    dropped_indices=list(set(dropped_indices))          
    indices = [i for i in range(len(states)) if i not in dropped_indices]
    states = [states[i] for i in indices]

    return states
def findParallelBrothers(states):
    orthogonal_regions =[state.child_region for state in states if state.child_region is not None]
    states_names = [state.name for state in states]
    if len(orthogonal_regions)>0:
        for region in orthogonal_regions:
            count = 0
            for regioni in region:
                count +=1
                paired_indexes=[]
                for child in regioni:
                    val = list(child.attrib)
                    id_elem = [elem for elem in val if "id" in elem]
                    source_elem = [elem for elem in val if "source" in elem]
                    target_elem = [elem for elem in val if "target" in elem]
                    val = [elem for elem in val if "type" in elem]
                    if len(val)==1 and "uml:State" in child.attrib[val[0]]:
                        comparison = list(set([states_names.index(name) for name in states_names if child.attrib['name'] in name ]))
                        paired_indexes.extend(comparison)
                for index_ in paired_indexes:
                    states[index_].orthogonal = True
                    states[index_].parallel = [brother for brother in paired_indexes if brother != index_]
    return states
def addPseudostateToState(transition_pairs,pseudostates,states):
    ids_pseudostate = [pseudostate.id for pseudostate in pseudostates]
    candidate_pseudostate = []
    for id in ids_pseudostate:
        pairs_pseudostate = []
        for pair in transition_pairs:
            if id in pair:
                pairs_pseudostate.append(pair)
        
        if len(pairs_pseudostate)==1:
            for pair in pairs_pseudostate:
                candidate_pseudostate.append(id)
    
    state_regions_child,state_regions_child_indexes = getChildRegionsExtended(states)
    for id in candidate_pseudostate:
        if pseudostates[ids_pseudostate.index(id)].parent_region in state_regions_child:
            try:
                index = state_regions_child_indexes[state_regions_child.index(pseudostates[ids_pseudostate.index(id)].parent_region)]
                pair = (states[index].id,id)
                transition_pairs.append(pair)
            except:
                pass
    return transition_pairs
def addStatetoStatebyPseudostate(transition_pairs,pseudostates):
    ids_pseudostate = [pseudostate.id for pseudostate in pseudostates ]
    for id in ids_pseudostate:
        pairs_pseudostate = []
        for pair in transition_pairs:
            if id in pair:
                pairs_pseudostate.append(pair)
        if len(pairs_pseudostate)==2:
            for pair in pairs_pseudostate:
                if id == pair[0]:
                    target = pair[1]    
                elif id == pair[1]:
                    source = pair[0]
            pair = (source,target)
            transition_pairs.append(pair)
    return transition_pairs
def addFromParentToChildren(transition_pairs,originalParentIds):
    
    for parent_id in originalParentIds:
        if parent_id is not None:
            if type(parent_id)==type([]):
                for parent_id in parent_id:
                    pairs_parents = []
                    for pair in transition_pairs:
                        if parent_id in pair:
                            pairs_parents.append(pair)
                   
                    if len(pairs_parents)==2:
                        source,target = 0,0
                        for pair in pairs_parents:
                            if parent_id == pair[0]:
                                target = pair[1]
                            elif parent_id == pair[1]:
                                source = pair[0]       
                        if source!= 0 and target !=0:
                            pair = (source,target)
                            transition_pairs.append(pair)
                            
            else:
                pairs_parents = []
                for pair in transition_pairs:
                    
                    if parent_id in pair:
                        pairs_parents.append(pair)
                
                if len(pairs_parents)==2:
                    source,target = 0,0
                    for pair in pairs_parents:
                        if parent_id == pair[0]:
                            target = pair[1]
                        elif parent_id == pair[1]:
                            source = pair[0] 
                    if source!= 0 and target !=0:
                        pair = (source,target)      
                        transition_pairs.append(pair)
                        
    return transition_pairs
def findOrthogonal(originalChildRegions):
    test = False
    for child in originalChildRegions:
        if len(child)>1:
            test=True
    return test
def findFork(transition_pairs,ids,originalIds,pseudostates):
    fork = False
    pseudostateIds= [pseudostate.id for pseudostate in pseudostates]
    for pseudostateId in pseudostateIds:
        count = 0
        for pair in transition_pairs:
            if pseudostateId==pair[0]:
                count+=1
        if count==2:
            fork = True
    return fork
def findJoin(transition_pairs,originalIds,originalNames,pseudostates):
    join = False
    pseudostateIds= [pseudostate.id for pseudostate in pseudostates]
    for pseudostateId in pseudostateIds:
        count = 0
        for pair in transition_pairs:
            if pseudostateId==pair[1]:
                count+=1
        if count==2:
            join = True
    return join
def getJoin(transition_pairs,originalIds,originalNames,pseudostates):
    join = []
    pseudostateIds= [pseudostate.id for pseudostate in pseudostates]
    for pseudostateId in pseudostateIds:
        count = 0
        for pair in transition_pairs:
            if pseudostateId==pair[1]:
                count+=1
        if count ==2:
            joinPseudostate=pseudostateId
            pairsWithPseudotate = [pair for pair in transition_pairs if pseudostateId==pair[1]]
            for pair in pairsWithPseudotate:
                originalIdIndex = originalIds.index(pair[0])
                join.append(originalNames[originalIdIndex])
            
    return join
def getFork(transition_pairs,originalIds,originalNames,pseudostates):
    fork = []
    pseudostateIds= [pseudostate.id for pseudostate in pseudostates]
    for pseudostateId in pseudostateIds:
        count = 0
        for pair in transition_pairs:
            if pseudostateId==pair[0]:
                count+=1
        if count ==2:
            forkPseudostate=pseudostateId
            pairsWithPseudotate = [pair for pair in transition_pairs if pseudostateId==pair[0]]
            for pair in pairsWithPseudotate:
                originalIdIndex = originalIds.index(pair[1])
                fork.append(originalNames[originalIdIndex])
    return fork
def getOrthogonal(originalChildRegions):
    stateAttrib = "uml:State"
    orthogonalStatesNames = []
    for regionList in originalChildRegions:
        for child in regionList:
            states=find_child(child,attribName=stateAttrib,exhaustive=True)
            orthogonalStatesNames.append([get_attrib_in_root(state,attribName="name") for state in states])
    return orthogonalStatesNames
def findDeepHistory(pseudostates):
    kinds = [pseudostate.kind for pseudostate in pseudostates]
    deepHistory=False
    if len(kinds)>0:
        for kind in kinds:
            if kind is not None:
                if "deep" in kind:
                    deepHistory = True
    return deepHistory
def addFromStatetoStateByOriginalState(transition_pairs,originalIds,ids):
    
    transition_pairs = list(set(list(transition_pairs)))
    differentIds = [idx for idx in originalIds if idx not in ids]
    for originalId in differentIds:
        evaluate = []
        for idx in ids:
            for pair in transition_pairs:
                if originalId in pair and idx in pair:
                    evaluate.append(pair)
        if len(evaluate)==2:
            paired = (evaluate[0][0],evaluate[1][1])
            if paired not in transition_pairs:
                transition_pairs.append(paired)
                
    return transition_pairs
def buildStatesTransitionsActivities(pseudostates,states,transitions,activities):
    
    transition_pairs = [(transition.source,transition.target) for transition in transitions]
    states,_ = build_states(states)
    parallel = findParallel(states)
    states = setParallel(states,parallel)
    states = findSetParent(states)
    transition_pairs = addPseudostateToState(transition_pairs,pseudostates,states)
    transition_pairs = addStatetoStatebyPseudostate(transition_pairs,pseudostates)
    
    originalIds = [state.id for state in states]
    originalNames = [state.name for state in states]
    originalParentIds = [state.parent_id for state in states]
    originalParentRegions = [state.parent_region for state in states]
    originalChildRegions = getChildRegions(states)
    
    states = clean_states(states)
    names = [state.name for state in states]
    ids = [state.id for state in states]
    activities_parent_name = [activity.name for activity in activities if activity.parent_id in ids]
    activities_name = [names[ids.index(activity.parent_id)] for activity in activities if activity.parent_id in ids]
    not_states_index = []
    states_index = []
    parentsIds = [states[i].parent_id for i in range(len(states))if states[i].parent_id is not None ]
    
    transition_pairs = addFromParentToChildren(transition_pairs,originalParentIds)
    transition_pairs = addFromStatetoStateByOriginalState(transition_pairs,originalIds,ids)
    

    if findOrthogonal(originalChildRegions):
        orthogonals = getOrthogonal(originalChildRegions) 
        
    else:
        orthogonals = None
    if findFork(transition_pairs,ids,originalIds,pseudostates):
        fork = getFork(transition_pairs,originalIds,originalNames,pseudostates)
    else:
        fork = None
        
    if findJoin(transition_pairs,originalIds,originalNames,pseudostates):
        join = getJoin(transition_pairs,originalIds,originalNames,pseudostates)
    else:
        join = None
        
    if findDeepHistory(pseudostates):
        deepHistory = True
    else:
        deepHistory = None
    
    return pseudostates,states,transition_pairs,activities,orthogonals,fork,join,deepHistory
def matchOrthogonalStates(orthogonals,states):
    stateNames = [state.name for state in states]
    statesOrthogonal = {}
    for name in stateNames:
        for orthogonal in orthogonals:
            if orthogonals.index(orthogonal) not in statesOrthogonal:
                statesOrthogonal[orthogonals.index(orthogonal)]=[]
            for subOrthogonal in orthogonal:
                if subOrthogonal in name:
                    statesOrthogonal[orthogonals.index(orthogonal)].append(name)
    statesOrthogonal = list(statesOrthogonal.values())
    return statesOrthogonal
def getProduct(listOfLists):
    lists = [len(subList) for subList in listOfLists]
    if np.all(np.array(lists)>1):
        return [element for element in product(*listOfLists)]
    else:
        theProduct = [element for subLists in listOfLists for element in subLists ]
        concat = ""
        for element in theProduct:
            
            if theProduct.index(element) != len(theProduct)-1:
                concat = concat+element+","
            else:
                concat = concat+element
        return [concat]

def getInputsByStates(transitions_pairs,states):
    statesIds = [state.id for state in states]
    inputs=[]
    for pair in transition_pairs:
        source,target = None,None
        if pair[0] in statesIds:
            source = "from_"+states[statesIds.index(pair[0])].name
        if pair[1] in statesIds:
            target = "_to_"+states[statesIds.index(pair[1])].name
        if source != None and target != None:
            inputs.append(source+target)
    return inputs
def getInputsByStatesNames(states):
    inputs = ["from_"+state+"_to_"+state2 for state in states for state2 in states if state!=state2 ]
    return inputs
def matchOrthogonalInputs(orthogonals,inputs):
    inputsCropped = [name.replace("from_","").replace("_to_","") for name in inputs]
    inputsOrthogonal = {}
    for name in inputsCropped:
        for orthogonal in orthogonals:
            count = 0 
            if orthogonals.index(orthogonal) not in inputsOrthogonal:
                inputsOrthogonal[orthogonals.index(orthogonal)]=[]
            
            for subOrthogonal in orthogonal:
                count = count+1 if  subOrthogonal in name else count
            if count>0:
                inputsOrthogonal[orthogonals.index(orthogonal)].append(inputs[inputsCropped.index(name)])
    inputsOrthogonal= list(inputsOrthogonal.values())
    return inputsOrthogonal
def getOutputsByStates(activities,states):
    activityParentIds = [activity.parent_id for activity in activities]
    stateIds = [state.id for state in states]
    outputs = {}
    for activityId in activityParentIds:
        if activityId in stateIds:
            stateName = states[stateIds.index(activityId)].name
            if stateName not in outputs:
                outputs[stateName]=activities[activityParentIds.index(activityId)].name
    
    return outputs
def matchOrthogonalOutputs(orthogonals,outputs):
    stateNames = list(outputs)
    outputNames = list(outputs.values())
    outputsOrthogonal = {}
    for name in stateNames:
        for orthogonal in orthogonals:
            if orthogonals.index(orthogonal) not in outputsOrthogonal:
                outputsOrthogonal[orthogonals.index(orthogonal)]=[]
            for subOrthogonal in orthogonal:
                if subOrthogonal in name:
                    outputsOrthogonal[orthogonals.index(orthogonal)].append(outputNames[stateNames.index(name)])
    outputsOrthogonal = list(outputsOrthogonal.values())
    return outputsOrthogonal
def matchNonOrthogonalOutputs(orthogonals,outputs):
    stateNames = list(outputs)
    outputNames = list(outputs.values())
    outputsOrthogonal = []
    for name in stateNames:
        count=0
        for orthogonal in orthogonals:
            for subOrthogonal in orthogonal:
                if subOrthogonal in name:
                    count +=1
        if count == 0:
            outputsOrthogonal.append(outputNames[stateNames.index(name)])
    return outputsOrthogonal
def getStatesNonOrthogonalStates(states,orthogonals):
    stateNames = [state.name for state in states]
    nonOrthogonalStates = []
    for name in stateNames:
        count = 0
        for orthogonal in orthogonals:
            for subOrthogonal in orthogonal:
                count = count + 1 if  subOrthogonal in name else count
        if count == 0:     
            nonOrthogonalStates.append(name)               
    return nonOrthogonalStates
def getStates(states):
    return [state.name for state in states]
def getInputs(transition_pairs,states):
    return ["from_"+states[states.index(pair[0])].name+"_to_"+states[states.index(pair[1])].name for pair in transition_pairs]
def createSystem(name,states,inputs,outputs):
    S=[State(state,[0,1])for state in states]
    I=[Input(input_,[0,1])for input_ in inputs]
    O=[Output(output,[0,1])for output in outputs]
    return System(name,S,I,O)
def rearrangeTuples(tuples):
    rearranged = []
    for subTuple in tuples:
        separator = ""
        separator = separator.join(subTuple)
        rearranged.append(separator)
    return rearranged
def rearrangeTuplesInputs(tuples):
    rearranged = []
    for subTuple in tuples:
        replaced = [input_.replace("from_","") for input_ in subTuple]
        index = [input_.find("_to_") for input_ in replaced]
        firstStates = []
        secondStates = []
        for i in range(len(subTuple)):
            firstStates.append(replaced[i][:index[i]])
            secondStates.append(replaced[i][index[i]+4:])
        aggregatedFirstStates = "".join(firstStates)
        aggregatedLastStates = "".join(secondStates)
        source = "from_"+aggregatedFirstStates
        target = "_to_"+aggregatedLastStates
        rearranged.append(source+target)
    return rearranged

def createSystemOrthogonal(name,states,inputs,outputs):
    
    stateTuples = [state for state in states if type(state)==type(tuple())]
    inputTuples = [input_ for input_ in inputs if type(input_)==type(tuple())]
    outputTuples = [output for output in outputs if type(output)==type(tuple())]
    states = rearrangeTuples(stateTuples)
    inputs = rearrangeTuplesInputs(inputTuples)
    outputs =rearrangeTuples(outputTuples)
    print(states,inputs,outputs)
    S=[State(state,[0,1])for state in states]
    I=[Input(input_,[0,1])for input_ in inputs]
    O=[Output(output,[0,1])for output in outputs]
    return System(name,S,I,O)
def buildSystem(name,pseudostates,states,transition_pairs,activities,orthogonals,fork,join,deepHistory):    
    
    
    if orthogonals is not None:
        
        nonOrthogonalStates= getStatesNonOrthogonalStates(states,orthogonals)
        inputs = getInputsByStates (transition_pairs,states)
        inputsOrthogonal = matchOrthogonalInputs(orthogonals,inputs)
        inputsTuples = getProduct(inputsOrthogonal)
        statesOrthogonal = matchOrthogonalStates(orthogonals,states)
        statesTuples = getProduct(statesOrthogonal)
        outputs = getOutputsByStates(activities,states)
        nonOrthogonalOutputs = matchNonOrthogonalOutputs(orthogonals,outputs)
        outputsOrthogonal = matchOrthogonalOutputs(orthogonals,outputs)
        outputsTuples = getProduct(outputsOrthogonal)
        
        if fork is not None or join is not None:
            totalStates = copy.deepcopy(nonOrthogonalStates)
            for state in statesTuples:
                totalStates.append(state)
            inputsTuples = getInputsByStatesNames(totalStates)
            
        else:
            system = createSystemOrthogonal(name,statesTuples,inputsTuples,outputsTuples)
            
    else:
        statesTuples = getStates(states)
        inputsTuples = getInputsByStates(transition_pairs,states)
        outputsTuples =  list(getOutputsByStates(activities,states).values())
        system = createSystem(name,statesTuples,inputsTuples,outputsTuples)
        if deepHistory is not None:
            
        else:
            system = createSystem(name,statesTuples,inputsTuples,outputsTuples)
    
    # elif deepHistory is not None:

if __name__=="__main__":
    # for fig in ['Fig1','Fig2','Fig3','Fig4','Fig5','Fig6']:
    for fig in ["Fig1","Fig2",'Fig3','Fig4']:
        print("\nTesting "+fig+"\n")
        tree = ET.parse(fig+'/com.nomagic.magicdraw.uml_model.model')
        root = tree.getroot()
        regions,model_name = find_state_machine_region(root)
        states = []
        transitions = []
        activities = []
        pseudostates = []
        systems=[]
        for region in regions:
            pseudostates,states,transitions,activities = search(region,pseudostates,states,transitions,activities)
            pseudostates,states,transition_pairs,activities,orthogonals,fork,join,deepHistory = buildStatesTransitionsActivities(pseudostates,states,transitions,activities)
            system = buildSystem(model_name,pseudostates,states,transition_pairs,activities,orthogonals,fork,join,deepHistory)