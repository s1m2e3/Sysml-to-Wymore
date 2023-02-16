from itertools import product
import networkx as nx 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def input_output_feedback(input_,output_):
    
    if input_.available_data == output_.available_data:
        
        input_.output = output_
        input_.feedback = True
        output_.feedback = True
        output_.input = input_
        
        if input_.current_system == output_.current_system:
            
            print("feedback on same system")
            input_.current_system.feedback = True
        
        else:

            input_.current_system.attached_systems[0].append(output_.current_system)
            input_.current_system.feedback = True
            output_.current_system.attached_systems[1].append(input_.current_system)
            
        return input_,output_

    else:
        raise ValueError("Input set doesn't match output set")
    
def check_name_uniqueness(objects_list):
    
    len_dict = len(objects_list)
    len_names = len(set([val.name for val in list(objects_list.values())]))
    if len_dict==len_names:
        pass
    else:
        raise ValueError("names are repeated")

class Input:

    def __init__(self,name,input_type,data,current_data=None,feedback=False,attached_output=None,current_system=None,attached_system=[]):
        
        self.name = name
        self.type = input_type 
        #sets of input data, they would be "RR" for any number in the real set
        #                    "II" for any integer
        #                    "CHAR" for any string
        #                    {} for any finite set of inputs // must use frozenset
        
        self.available_data = list(set(data))
        if self.type == "RR" and np.all(np.array([type(i)==type(1.) for i in self.available_data])==True):
            pass
        elif self.type == "II" and np.all(np.array([type(i)==type(1) for i in self.available_data])==True):
            pass
        elif self.type == "CHAR" and np.all(np.array([type(i)==type("1.") for i in self.available_data])==True):
            pass
        else:
            raise ValueError("type and provided set don't match")
        #current input data
        self.data = current_data
        #whether or not the input stream is feedback of another output
        self.feedback = feedback
        #output object connected to the input object through feedback
        self.output = attached_output
        #system which receives the input
        self.current_system = current_system
        #attached systems through coupling to the system receiving the input
        self.attached_system = attached_system
       

class Output:
    
    def __init__(self,name,output_type,data,current_data=None,feedback=False,attached_input=None,current_system=None,attached_system=[]):
        
        #similar behavior as the Input class
        self.name = name
        self.type = output_type 
        #sets of input data, they would be "RR" for any number in the real set
        #                    "II" for any integer
        #                    "CHAR" for any string
        #                    {} for any finite set of inputs // must use frozenset
        
        self.available_data = list(set(data))
        if self.type == "RR" and np.all(np.array([type(i)==type(1.) for i in self.available_data])==True):
            pass
        elif self.type == "II" and np.all(np.array([type(i)==type(1) for i in self.available_data])==True):
            pass
        elif self.type == "CHAR" and np.all(np.array([type(i)==type("1.") for i in self.available_data])==True):
            pass
        else:
            raise ValueError("type and provided set don't match")
        
        self.data = current_data
        self.feedback = feedback
        self.input = attached_input
        self.current_system = current_system
        self.attached_system = attached_system
        

class State:

    def __init__(self,name,state_type,data,current_data=None,current_system=None,attached_system=None):
        
        self.name = name
        self.type = state_type
        self.available_data = list(set(data))
        if self.type == "RR" and np.all(np.array([type(i)==type(1.) for i in self.available_data])==True):
            pass
        elif self.type == "II" and np.all(np.array([type(i)==type(1) for i in self.available_data])==True):
            pass
        elif self.type == "CHAR" and np.all(np.array([type(i)==type("1.") for i in self.available_data])==True):
            pass
        else:
            raise ValueError("type and provided set don't match")
        
        self.data = current_data
        self.current_system = current_system
        self.attached_system = attached_system


class TransitionFunction:
    def __init__(self,states,inputs,function):

        #states tuple is not the states objects but the state themselves
        self.states = states
        #inputs tuple is not the input objects but the inputs themselves
        self.inputs = inputs
        self.function = function
        try:
            self.function(states,self.inputs)
        except:
            raise ValueError("function is not computing given states tuple and inputs tuple")

class ReadoutFunction:
    def __init__(self,states,function):

        #states tuple is not the states objects but the state themselves
        self.states = states
        self.function = function
        try:
            self.function(states)
        except:
            raise ValueError("function is not computing given states tuple")



class System:

    def __init__(self,states=[],inputs=[],outputs=[],name="system"):
        
        #inputs have the following structure: {0:Input_object,1:Input_object,...}
        #It will be required that all the non-feedback inputs go before the feedback inputs
        #where each of the indexes is the stream of inputs. Similarly for the outputs
        #{0: Output_object, 1:Output_object,...}
        #states have the following structure: {0:state_object,1:state_object,...} 
        #  are just described in the states set, and the current state could only be one element of the states,
        #however one element of the states could be a vector or a higher dimension array
        
        #sets of states behave similarly as inputs and outputs, would be: 
        #                         "RR" for any number in the real set
        #                         "II" for any integer
        #                         "CHAR" for any string
        #                         {} for any finite set of inputs // must use frozenset

        #check name uniqueness of S,I,O
        
        map(check_name_uniqueness,[states,inputs,outputs])
        self.name=name

        names = [state.name for state in states]
        self.states = dict(zip(names,states))
        
        for state in self.states.values():
            state.current_system = self  

        names = [input_.name for input_ in inputs]
        self.inputs = dict(zip(names,inputs))

        for input_ in self.inputs.values():
            input_.current_system = self

        names = [output.name for output in outputs]
        self.outputs = dict(zip(names,outputs))

        for output in self.outputs.values():
            output.current_system = self
        del(names)

        self.all_states = self.get_all_possible(self.states)
        self.all_inputs = self.get_all_possible(self.inputs)
        self.all_outputs = self.get_all_possible(self.outputs)

        self.states_x_inputs = list(product(self.all_states,self.all_inputs))
        
        self.transition_functions = {}
        self.readout_functions = {}
        self.current_state = None
        self.states_graph = None
        self.attached_systems = {0:[]}
        
        self.feedback = sum([input_.feedback for input_ in self.inputs.values()])>0

    def get_all_possible(self,sets):

        object_set = list(sets)
        object_set = [list(sets[i].available_data) for i in range(len(object_set))]
        final = []
        for element in product(*object_set):
            final.append(element)
        return final

    

    def add_transition_function(self, function):
        
        #function objects have the tuple state and input.
        #validate that state and input in function exists in states x input set:
        for state in function.states:
            if function.states[state] in self.states[state].available_data:
                pass
            else:
                raise ValueError("state not in defined states dictionary")
        for input_ in function.inputs:
            if function.inputs[input_] in self.inputs[input_].available_data:
                pass
            else:
                raise ValueError("input not in defined inputs dictionary")
        
        try:
            next_state = function.function(function.states,function.inputs)

            for state in next_state:
                if next_state[state] in self.states[state].available_data:
                    pass
                else:
                    raise ValueError("computed state not in defined states dictionary")
        
            print("properly defined transition function added to transition functions")
            self.transition_functions[(function.states,function.inputs)]=function.function
            
        except:
            raise Exception("function didn't compute")    
        

    def add_readout_function(self, function):
        
        #function objects have the tuple state 
        #validate that state exists in states set:
        if function.states_tuple in self.all_states:
            try:
                output = function.function(function.states_tuple)
                if output in self.all_outputs: 
                    print("properly defined readout function added to readout functions")
                    self.readout_functions[function.states_tuple]=function.function
                else:
                    print(output)
                    print(self.all_outputs)
                    raise ValueError("function didn't compute valid state")
            except:
                raise Exception("function didn't compute")
        else:
            raise ValueError("either state or inputs not in states_x_inputs set")

    def get_num_nofeed(self):
        return sum([Input.feedback for Input in self.inputs])
    def prep_transition(self,sys_input):
        for i in range(len(sys_input)):
            self.inputs[i].data = sys_input[i]
            print("input data updated")
        current_input = tuple([input_.data for input_ in self.inputs.values()])
        return current_input
    
    def check_current_state(self,initial_state=None):
        if initial_state==None and self.current_state==None:
            return False
        elif initial_state != None:
            self.current_state = initial_state
            return True
        else:
            return True

    def transition(self,sys_input,initial_state=None):
        
        #initial_state is a tuple of states
        #sys input would be the tuple [(Input.name:input_object1.data)},input_object2.data,...) containing only data from non-feedback inputs
        #check that input_objects are inside their validated sets given feedback or not:
        
        if self.check_current_state(initial_state):
            
            if self.feedback:

                #get latest output from attached systems
                list_sys = []
                list_sys.append(sys_input)
                        
                for i in range(len(self.inputs)):
                    if self.inputs[i].feedback:
                        #get system of output attached to input
                        attached_system = self.inputs[i].output.current_system
                        #update output of attached systems
                        if attached_system.current_state != None:
                            attached_system_outputs=list(attached_system.readout_functions[attached_system.current_state](attached_system.current_state))
                            for j in range(len(attached_system.outputs)):
                                attached_system.outputs[list(attached_system.outputs)[j]].data = attached_system_outputs[j]
                                print("output data updated")
                        else:
                            raise ValueError("attached systems can't provide output without existing state")    
                        list_sys.append(self.inputs[i].output.data)
                sys_input = tuple(list_sys)  
                print(sys_input)
                print("current state:", self.current_state)
                print("updating stored inputs")
                current_input = self.prep_transition(sys_input)
                self.current_state=self.transition_functions[(self.current_state,current_input)](self.current_state,current_input)
                print("transitioned to state:",self.current_state)

            elif sys_input in self.all_inputs:
            
                if self.check_current_state(initial_state):
                    print("current state:", self.current_state)
                    print("updating stored inputs")
                    current_input = self.prep_transition(sys_input)
                    self.current_state=self.transition_functions[(self.current_state,current_input)](self.current_state,current_input)
                    print("transitioned to state:",self.current_state)

            else:
                raise ValueError("input stream not in input set")
        else:
            raise ValueError("can't transition without initial state")
        

    def validate_system(self):
         
         
        if len(self.transition_functions)>=len(self.states)-1 and len(self.readout_functions)==len(self.all_states):

            transition_index = list(self.transition_functions)
            edges = [(pair[0],self.transition_functions[pair](pair[0],pair[1])) for pair in transition_index]
            edges_labels = [pair[1] for pair in transition_index]
            edges_labels = dict(zip(edges,edges_labels))
            self.states_graph = nx.Graph()
            self.states_graph.add_edges_from(edges)
            reachability = nx.is_connected(self.states_graph)
            
            return reachability
        else:
            raise Exception("need more transition or readout functions")
    
    def run_experiment(self,time_steps,inputs_vector,initial_state=None):

        if self.validate_system():
            table = {}
            if initial_state is not None:
                self.current_state = initial_state
            elif self.current_state is not None: 
                pass 
            else: 
                raise Exception("can't run experiment without initial state")
            for time_step in np.arange(time_steps):
                table[time_step] = [self.current_state,inputs_vector[time_step],self.readout_functions[self.current_state](self.current_state)]
                try:
                    self.transition(inputs_vector[time_step])
                except:
                    raise ValueError("transition from current state with input not defined in transition functions")
            return table 
        else:
            raise Exception("can't run experiment without proper validation")

    def couple(self,system_1,system_2,type_):
        
        # The function re-defines INPUTS,STATES AND OUTPUTS given systems.
        # Addtionally, the function recomposes transition functions and readout functions
        # By definition system_1 is the one whose input comes from system_2's output
        
        if system_1.name == system_2.name:
            raise ValueError("names of the coupled systems can't be the same")    
        
        else:
            
            system_1.attached_systems[0].append(system_2)
            system_2.attached_systems[0].append(system_1)
            system_2_inputs_name = [string + system_2.name for string in map(str,list(system_2.inputs))]
            system_2_outputs_name = [string + system_2.name for string in map(str,list(system_2.outputs))]
            system_2_states_name = [string + system_2.name for string in map(str,list(system_2.states))]
            
            if type_ == "attachment":
                
                system_1.inputs.update(dict(zip(system_2_inputs_name,system_2.inputs.values())))
                system_1.outputs.update(dict(zip(system_2_outputs_name,system_2.outputs.values())))
                system_1.states.update(dict(zip(system_2_states_name,system_2.states.values())))
                system_1.all_inputs = system_1.get_all_possible(system_1.inputs)
                system_1.all_outputs = system_1.get_all_possible(system_1.outputs)
                system_1.all_states = system_1.get_all_possible(system_1.states)
                system_1.states_x_inputs = list(product(system_1.all_states,system_1.all_inputs))

                return system_1,system_2
                

            elif type_ == "composing":
                
                

                system_1_inputs_name = [string + system_1.name for string in map(str,list(system_1.inputs))]
                system_1_outputs_name = [string + system_1.name for string in map(str,list(system_1.outputs))]
                system_1_states_name = [string + system_1.name for string in map(str,list(system_1.states))]
            
            
                I_labels = system_1_inputs_name.extend(system_2_inputs_name)
                I_values = list(system_1.inputs.values()).extend(system_2.inputs.values())
                I = dict(zip(I_labels,I_values))
                
                O_labels = system_1_outputs_name.extend(system_2_outputs_name)
                O_values = list(system_1.outputs.values()).extend(system_2.outputs.values())
                O = dict(zip(O_labels,O_values))
                
                S_labels = system_1_states_name.extend(system_2_states_name)
                S_values = list(system_1.states.values()).extend(system_2.states.values())
                S = dict(zip(S_labels,S_values))
            
                name = system_1.name + "_" + system_2.name
                
                coupled_system = System(S,I,O,name)

            return coupled_system, system_1,system_2