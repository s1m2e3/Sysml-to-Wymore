from sysml_submethods import *

      
if __name__=="__main__":
    filename = 'Large_stm.xml'
    tree = ET.parse(filename)
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
        print([state.name for state in states])
        print(orthogonals)
        system = buildSystem(model_name,pseudostates,states,transition_pairs,activities,orthogonals,fork,join,deepHistory)
        # if fig == "Fig1":
        #     currentState = (1,0)
        #     inputVector = [(1,0),(0,1)]
        #     system.setCurrentState(currentState)
        #     system.runExperiment(inputsVector=inputVector)
        