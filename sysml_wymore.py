import xml.etree.ElementTree as ET
from system import *
from itertools import product
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import tournament
from itertools import permutations 
from itertools import product 
import copy
from sysml_subclasses import *
from sysml_submethods import *

        


if __name__=="__main__":
    for fig in ['Fig1','Fig2','Fig3','Fig4','Fig5','Fig6']:
    # for fig in ["Fig6"]:
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
            states,transition_pairs,activities,orthogonals,fork,join = buildStatesTransitionsActivities(pseudostates,states,transitions,activities)
            system = buildSystem(states,transition_pairs,activities,orthogonals,fork,join)        # if fig == "Fig1":
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

