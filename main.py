import pandas as pd
from system import *
#from system import Tran_func

if __name__=="__main__":
    
    S = [State(name="open?",state_type="II",data=[0,1]),State(name="key?",state_type="II",data=[0,1])] 

    I = [Input(name="try_open?",input_type="II",data=[0,1]),Input(name="present_key?",input_type="II",data=[0,1])]

    O = [Output(name="success?",output_type="II",data=[0,1])]

    sys = System(states=S,inputs=I,outputs=O)
    
    #dont try to open without a key and dont 
    func = lambda states_dict,inputs_dict: {"open?":0,"key":0}
    t1 = TransitionFunction(states_dict={"open?":0,"key":0},inputs_dict={"try_open?":0,"present_key":0},function=func)
    func = lambda states_dict,inputs_dict: {"open?":0,"key":1}
    t2 = TransitionFunction(states_dict={"open?":0,"key":0},inputs_dict={"try_open?":0,"present_key":1},function=func)
    func = lambda states_dict,inputs_dict: {"open?":0,"key":0}
    t3 = TransitionFunction(states_dict={"open?":0,"key":0},inputs_dict={"try_open?":1,"present_key":0},function=func)
    func = lambda states_dict,inputs_dict: {"open?":1,"key":1}
    t4 = TransitionFunction(states_dict={"open?":0,"key":0},inputs_dict={"try_open?":1,"present_key":1},function=func)
    func = lambda states_dict,inputs_dict: {"open?":0,"key":1}
    t5 = TransitionFunction(states_dict={"open?":0,"key":1},inputs_dict={"try_open?":0,"present_key":0},function=func)
    func = lambda states_dict,inputs_dict: {"open?":1,"key":1}
    t7 = TransitionFunction(states_dict={"open?":0,"key":1},inputs_dict={"try_open?":1,"present_key":0},function=func)
    func = lambda states_dict,inputs_dict: {"open?":1,"key":0}
    t9 = TransitionFunction(states_dict={"open?":1,"key":0},inputs_dict={"try_open?":0,"present_key":0},function=func)
    func = lambda states_dict,inputs_dict: {"open?":1,"key":1}
    t10 = TransitionFunction(states_dict={"open?":1,"key":0},inputs_dict={"try_open?":0,"present_key":1},function=func)
    func = lambda states_dict,inputs_dict: {"open?":1,"key":0}
    t11 = TransitionFunction(states_dict={"open?":1,"key":0},inputs_dict={"try_open?":1,"present_key":0},function=func)
    func = lambda states_dict,inputs_dict: {"open?":1,"key":1}
    t12 = TransitionFunction(states_dict={"open?":1,"key":0},inputs_dict={"try_open?":1,"present_key":1},function=func)
    func = lambda states_dict,inputs_dict: {"open?":1,"key":0}
    t13 = TransitionFunction(states_dict={"open?":1,"key":1},inputs_dict={"try_open?":0,"present_key":0},function=func)
    func = lambda states_dict,inputs_dict: {"open?":1,"key":1}
    t14 = TransitionFunction(states_dict={"open?":1,"key":1},inputs_dict={"try_open?":0,"present_key":1},function=func)
    func = lambda states_dict,inputs_dict: {"open?":1,"key":0}
    t15 = TransitionFunction(states_dict={"open?":1,"key":1},inputs_dict={"try_open?":1,"present_key":0},function=func)
    for t in [t1,t2,t3,t4,t5,t7,t9,t10,t11,t12,t13,t14,t15]:
        
        sys.add_transition_function(t)
    
    func = lambda states_dict: {"success":0}
    t1 = ReadoutFunction(states_dict={"open?":0,"key":0},function=func)
    func = lambda states_dict: {"success":0}
    t2 = ReadoutFunction(states_dict={"open?":0,"key":1},function=func)
    func = lambda states_dict: {"success":0}
    t3 = ReadoutFunction(states_dict={"open?":1,"key":0},function=func)
    func = lambda states_dict: {"success":1}
    t4 = ReadoutFunction(states_dict={"open?":1,"key":1},function=func)
    for t in [t1,t2,t3,t4]:
        sys.add_readout_function(t)
    I[1],O[0]=input_output_feedback(I[1],O[0])
    table = pd.DataFrame.from_dict(sys.run_experiment(5,[{(1)},(0),(1),(1),(1)],(0,1))).T
    table.columns = ["current_state","input","output"]
    print(table)
    


