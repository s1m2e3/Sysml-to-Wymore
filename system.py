from itertools import product
import networkx as nx 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def input_output_feedback(input_,output_):
    
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
        self.order = 0

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
        self.order = 0

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
    def __init__(self,states_tuple,inputs_tuple,function):

        #states tuple is not the states objects but the state themselves
        self.states_tuple = states_tuple
        #inputs tuple is not the input objects but the inputs themselves
        self.inputs_tuple = inputs_tuple
        self.function = function
        try:
            self.function(states_tuple,self.inputs_tuple)
        except:
            raise ValueError("function is not computing given states tuple and inputs tuple")

class ReadoutFunction:
    def __init__(self,states_tuple,function):

        #states tuple is not the states objects but the state themselves
        self.states_tuple = states_tuple
        self.function = function
        try:
            self.function(states_tuple)
        except:
            raise ValueError("function is not computing given states tuple")

class System:

    def __init__(self,states={},inputs={},outputs={}):
        
        #inputs have the following structure: {0:Input_object,1:Input_object,...}
        #It will be required that all the non-feedback inputs go before the feedback inputs
        #where each of the indexes is the stream of inputs. Similarly for the outputs
        #{0: Output_object, 1:Output_object,...}
        #states have the following structure: {0:state_object,1:state_object,...} 
        #  are just described in the states set, and the current state could only be one element of the states,
        #however one element of the states could be a vector or a higher dimension array

        compare = []
        for stream_index in inputs:
            if not inputs[stream_index].feedback:
                compare.append(stream_index)
         
        if np.all(np.array(compare)!=np.arange(len(compare))):
            raise ValueError("all not-feedback inputs must be written after the feedback inputs")

        #sets of states behave similarly as inputs and outputs, would be: 
        #                         "RR" for any number in the real set
        #                         "II" for any integer
        #                         "CHAR" for any string
        #                         {} for any finite set of inputs // must use frozenset

        self.states = states
        order = 0
        for state in self.states.values():
            state.current_system = self  
            state.order = order
            order+=1
        self.inputs = inputs
        order = 0
        for input_ in self.inputs.values():
            input_.current_system = self
            input_.order = order
            order +=1
        self.outputs = outputs
        order = 0
        for output in self.outputs.values():
            output.current_system = self
            output.order = order
            order += 1
        del(order)
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
        if (function.states_tuple,function.inputs_tuple) in self.states_x_inputs:
            try:
                next_state = function.function(function.states_tuple,function.inputs_tuple)
                if next_state in self.all_states: 
                    print("properly defined transition function added to transition functions")
                    self.transition_functions[(function.states_tuple,function.inputs_tuple)]=function.function
                else:
                    raise ValueError("function didn't compute valid state")
            except:
                raise Exception("function didn't compute")
        else:
            raise ValueError("either state or inputs not in states_x_inputs set")

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
            current_input = tuple([input_.data for input_ in self.inputs])
        return current_input
    
    def transition(self,sys_input,initial_state=None):
        #initial_state is a tuple of states
        #sys input would be the tuple (input_object1.data,input_object2.data,...) containing only data from non-feedback inputs
        #check that input_objects are inside their validated sets given feedback or not:
        if self.check_current_state(initial_state):
            
            if self.feedback:

                #get latest output from attached systems
                
                for i in range(len(self.inputs)):
                    if self.inputs[i].feedback:
                        #get system of output attached to input
                        attached_system = self.inputs[i].output.current_system
                        #update output of attached systems
                        if attached_system.current_state != None:
                            attached_system_outputs=list(attached_system.readout_functions[attached_system.current_state])
                            for j in range(len(attached_system.outputs)):
                                attached_system.outputs[list(attached_system.outputs)[j]].data = attached_system_outputs[j]
                        else:
                            raise ValueError("attached systems can't provide output without existing state")    
                        sys_input = sys_input + (self.inputs[i].output.data,)  
            
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
            fig, ax = plt.subplots(figsize=(15,8))
            nx.draw(self.states_graph,pos=nx.shell_layout(self.states_graph),with_labels=True,node_size=[1000 for state in self.states_graph.nodes],width=3)
            nx.draw_networkx_edge_labels(self.states_graph,pos=nx.shell_layout(self.states_graph),label_pos=0.5,font_color='red', font_size=16, font_weight='bold',edge_labels=edges_labels)
            plt.savefig("graph.png")
            return True
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
                self.current_state = self.transition_functions[(self.current_state,inputs_vector[time_step])](self.current_state,inputs_vector[time_step])
            return table 
        else:
            raise Exception("can't run experiment without proper validation")

    # def couple(self,recipes={},system2=None,new_states={},new_inputs={},new_outputs={}):
    #     #check recipes are properly created
    #     """
    #     four type of recipes exist, output 1 onto input 1, output 1 onto 2, output 2 onto input 2, output 2 onto input 2
    #     the recipes dictionary has the following shape: recipes = {(a,b):(output of system a,input of system b)}
    #     """
        


    #     #check pure feedback loops:
    #     for recipe in recipes:
    #         if recipe == (1,1):
    #             print("pure feedback coupling of system 1")
    #             if recipes[recipe][0] in self.outputs and recipes[recipe][1] in self.inputs:
    #                 print("updating transition function from ")
    #             else:
    #                 raise ValueError(" inputs and outputs don't match recipe")
                
    #             except:
                
    #         elif recipe == (2,2):
    #             print("pure feedback coupling of system 2")
    #         elif recipe == (1,2):
    #             print("output 1 onto system 2")
    #         elif recipe == (2,1):
    #             print("output 2 onto system 1")