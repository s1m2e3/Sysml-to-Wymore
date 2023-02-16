import pandas as pd
from system import *
#from system import Tran_func

if __name__=="__main__":
    
    S = {0:State(name="open?",state_type="II",data=[0,1]),1:State(name="key?",state_type="II",data=[0,1])} 

    I = {0:Input(name="try_open?",input_type="II",data=[0,1]),1:Input(name="present_key?",input_type="II",data=[0,1])} 

    O = {0:Output(name="success?",output_type="II",data=[0,1])} 

    sys = System(states=S,inputs=I,outputs=O)
    
    #dont try to open without a key and dont 
    func = lambda states_tuple,inputs_tuple: (0,0)
    t1 = TransitionFunction(states_tuple=(0,0),inputs_tuple=(0,0),function=func)
    func = lambda states_tuple,inputs_tuple: (0,1)
    t2 = TransitionFunction(states_tuple=(0,0),inputs_tuple=(0,1),function=func)
    func = lambda states_tuple,inputs_tuple: (0,0)
    t3 = TransitionFunction(states_tuple=(0,0),inputs_tuple=(1,0),function=func)
    func = lambda states_tuple,inputs_tuple: (1,1)
    t4 = TransitionFunction(states_tuple=(0,0),inputs_tuple=(1,1),function=func)
    func = lambda states_tuple,inputs_tuple: (0,1)
    t5 = TransitionFunction(states_tuple=(0,1),inputs_tuple=(0,0),function=func)
    func = lambda states_tuple,inputs_tuple: (1,1)
    t7 = TransitionFunction(states_tuple=(0,1),inputs_tuple=(1,0),function=func)
    func = lambda states_tuple,inputs_tuple: (1,0)
    t9 = TransitionFunction(states_tuple=(1,0),inputs_tuple=(0,0),function=func)
    func = lambda states_tuple,inputs_tuple: (1,1)
    t10 = TransitionFunction(states_tuple=(1,0),inputs_tuple=(0,1),function=func)
    func = lambda states_tuple,inputs_tuple: (1,0)
    t11 = TransitionFunction(states_tuple=(1,0),inputs_tuple=(1,0),function=func)
    func = lambda states_tuple,inputs_tuple: (1,1)
    t12 = TransitionFunction(states_tuple=(1,0),inputs_tuple=(1,1),function=func)
    func = lambda states_tuple,inputs_tuple: (1,0)
    t13 = TransitionFunction(states_tuple=(1,1),inputs_tuple=(0,0),function=func)
    func = lambda states_tuple,inputs_tuple: (1,1)
    t14 = TransitionFunction(states_tuple=(1,1),inputs_tuple=(0,1),function=func)
    func = lambda states_tuple,inputs_tuple: (1,0)
    t15 = TransitionFunction(states_tuple=(1,1),inputs_tuple=(1,0),function=func)
    for t in [t1,t2,t3,t4,t5,t7,t9,t10,t11,t12,t13,t14,t15]:
        sys.add_transition_function(t)
    
    func = lambda states_tuple: (0,)
    t1 = ReadoutFunction(states_tuple=(0,0),function=func)
    func = lambda states_tuple: (0,)
    t2 = ReadoutFunction(states_tuple=(0,1),function=func)
    func = lambda states_tuple: (0,)
    t3 = ReadoutFunction(states_tuple=(1,0),function=func)
    func = lambda states_tuple: (1,)
    t4 = ReadoutFunction(states_tuple=(1,1),function=func)
    for t in [t1,t2,t3,t4]:
        sys.add_readout_function(t)
    input_output_feedback(I[1],O[0])
    table = pd.DataFrame.from_dict(sys.run_experiment(5,[(1),(0),(1),(1),(1)],(0,1))).T
    table.columns = ["current_state","input","output"]
    print(table)
    

    # # tf1=Tran_func(lambda a: sum(a))
    # # tf1.validate((1,2))
    # # tf1.validate((1,"a"))
    # #tf2=
    # f_t = lambda a:sum(a)
    # f_r = lambda a:str(a)
    # system = System(S,I,O)
    # system.add_transition_function((1,0),f_t)
    # system.add_readout_function(1,f_r)
    
    

