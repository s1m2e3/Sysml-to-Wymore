from system import System
from func import Func
from system import Input
from system import Output
#from system import Tran_func

if __name__=="__main__":
    
    S = {1,0}
    I = {1:Input(4),2:Input(3),3:Input(feedback=True)}
    O = {1:Output(),2:Output(),3:Output()}
    # tf1=Tran_func(lambda a: sum(a))
    # tf1.validate((1,2))
    # tf1.validate((1,"a"))
    #tf2=
    f_t = lambda a:sum(a)
    f_r = lambda a:str(a)
    system = System(S,I,O)
    system.add_transition_function((1,0),f_t)
    system.add_readout_function(1,f_r)
    
    

