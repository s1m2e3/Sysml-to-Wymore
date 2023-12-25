from sysml_submethods import *

        



if __name__=="__main__":
    for fig in ['Fig1','Fig2','Fig3','Fig4','Fig5','Fig6']:
    
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
            if fig == "Fig1":
                currentState = (1,0)
                inputVector = [(1,0),(0,1)]
                system.setCurrentState(currentState)
                system.runExperiment(inputsVector=inputVector)
            elif fig == "Fig2":
                currentState = (0,0,0,1)
                inputVector = [(1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),\
                               (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),\
                               (0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),\
                               (0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),\
                               (0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),\
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),\
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0),\
                               (0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0),\
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0),\
                               (0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),\
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0),\
                               (0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0),\
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0),\
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0),\
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0),\
                               (0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0)]
                system.setCurrentState(currentState)
                system.runExperiment(inputsVector=inputVector)
                
            elif fig == "Fig3":
                currentState = (1,0,0)
                inputVector = [(1, 0, 0, 0, 0),\
                               (0, 0, 1, 0, 0),\
                               (0, 0, 0, 0, 1),\
                               (0, 1, 0, 0, 0),\
                               (1, 0, 0, 0, 0),\
                               (0, 0, 1, 0, 0),\
                               (0, 0, 0, 1, 0),\
                               (1, 0, 0, 0, 0)]    
                system.setCurrentState(currentState)
                system.runExperiment(inputsVector=inputVector)
            elif fig == "Fig4":
                currentState = (1,0,0,0)
                inputVector = [(1, 0, 0, 0, 0, 0),\
                               (0, 0, 1, 0, 0, 0),\
                               (0, 0, 0, 0, 1, 0),\
                               (0, 1, 0, 0, 0, 0),\
                               (1, 0, 0, 0, 0, 0),\
                               (0, 0, 1, 0, 0, 0),\
                               (0, 0, 0, 1, 0, 0),\
                               (0, 0, 0, 0, 0, 1)]
                system.setCurrentState(currentState)
                system.runExperiment(inputsVector=inputVector)
            elif fig == "Fig5":
                currentState = (1,0)
                inputVector = [(1,0)]
                system.setCurrentState(currentState)
                system.runExperiment(inputsVector=inputVector)
            elif fig == "Fig6":
                currentState = (0,1)
                inputVector = [(0,1)]
                system.setCurrentState(currentState)
                system.runExperiment(inputsVector=inputVector)                