import itertools
import pandas as pd
import numpy as np 
class State:
    def __init__(self,name,availableStates,currentState=None):
        self.name = name
        self.availableStates = availableStates
        self.currentState = currentState
class Input:
    def __init__(self,name,availableInputs):
        self.name = name
        self.availableInputs = availableInputs
class Output:
    def __init__(self,name,availableOutputs):
        self.name = name
        self.availableOutputs = availableOutputs
class System:
    def __init__(self,name,States,Inputs,Outputs):
        self.name = name
        self.states = States
        self.inputs = Inputs
        self.outputs = Outputs
        self.transitionFunctions = {}
        self.readoutFunctions = {}
        self.subSystems = {}
        self.currentState = None    
    def addTransitionFunction(self,next,states,inputs):
        if states in self.getAllPossibleStates():
            if inputs in self.getAllPossibleInputs():
                pass
            else:
                raise ValueError("inputs not in all possible inputs combinations")
        else:
            raise ValueError("states not in all possible states combinations")
        
        if next not in self.getAllPossibleStates():
            raise ValueError("new state not in all possible states combinations")
        
        if states not in self.transitionFunctions:
            self.transitionFunctions[states]={}
            self.transitionFunctions[states][inputs]=next
        else:
            self.transitionFunctions[states][inputs]=next
     
    def addReadoutFunction(self,output,states):
        if states in self.getAllPossibleStates():
            pass
        else:
            raise ValueError("states not in all possible states combinations")
        
        if output not in self.getAllPossibleOutputs():
            raise ValueError("output not in all possible states combinations")
        
        self.readoutFunctions[states]=output
    def setCurrentState(self,state):
        if state in self.getAllPossibleStates():
            self.currentState = state
        else:
            raise ValueError("setted state not in all possible states combinations")
    def getAllPossibleStates(self):
        existing = []
        possible = []
        for state in self.states:
            possible.append(tuple(state.availableStates))
        for element in itertools.product(*possible):
            if sum(element)==1:
                existing.append(element)
        return existing
    def getAllPossibleInputs(self):
        existing = []
        possible = []
        for input_ in self.inputs:
            possible.append(tuple(input_.availableInputs))
        for element in itertools.product(*possible):
            if sum(element)==1:
                existing.append(element)
        return existing
    def getAllPossibleOutputs(self):
        existing = []
        possible = []
        for output in self.outputs:
            possible.append(tuple(output.availableOutputs))
        for element in itertools.product(*possible):
            if sum(element)==1:
                existing.append(element)
        return existing
    def transition(self,inputs):
        self.setCurrentState(self.transitionFunctions[self.currentState][inputs]) 
    def runExperiment(self,inputsVector):
        if self.currentState==None:
            raise ValueError("have to set up current state")
        experimentTable = {}
        for i in range(len(inputsVector)):
            inputs = inputsVector[i]
            prev = self.currentState
            self.transition(inputs)    
            new = self.currentState
            outputs = self.readoutFunctions[new]
            nameInputs = self.inputs[inputs.index(1)].name
            nameNewStates = self.states[new.index(1)].name
            namePrevStates = self.states[prev.index(1)].name
            nameOutputs =self.outputs[outputs.index(1)].name
            experimentTable[i]={"previous states": namePrevStates,"new states":nameNewStates, "inputs": nameInputs,"outputs":nameOutputs}
            
        print(pd.DataFrame.from_dict(experimentTable).T)    
    
# s1 = State("s1",[0,1])
# i1 = Input("i1",[0,1])
# o1 = Output("o1",[0,1])
# s2 = State("s2",[0,1])
# i2 = Input("i2",[0,1])
# o2 = Output("o2",[0,1])
# states = [s1,s2]
# inputs = [i1,i2]
# outputs = [o1,o2]
# system = System("system1",states,inputs,outputs)


# system.addTransitionFunction(lambda:(1,1),states=(1,0),inputs=(0,1))
# system.addTransitionFunction(lambda:(1,1),states=(0,1),inputs=(1,0))
# system.addTransitionFunction(lambda:(0,1),states=(0,0),inputs=(0,1))
# system.addReadoutFunction(lambda:(0,1),states=(0,1))
# system.addReadoutFunction(lambda:(1,0),states=(1,0))
# system.addReadoutFunction(lambda:(0,0),states=(0,0))
# system.addReadoutFunction(lambda:(1,1),states=(1,1))
# system.setCurrentState((0,0))
# system.runExperiment([(0,1),(1,0)])