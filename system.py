from itertools import product
import networkx as nx 
import numpy as np

class Input:
    def __init__(self,data,current_data=None,feedback=False,attached_output=None,current_system=None,attached_system=None):
        
        #sets of input data, they would be "RR" for any number in the real set
        #                    "II" for any integer
        #                    "CHAR" for any string
        #                    {} for any finite set of inputs // must use frozenset
        self.available_data = data
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
    def __init__(self,data,current_data=None,feedback=False,attached_input=None,current_system=None,attached_system=None):
        
        #similar behavior as the Input class
        self.available_data = data
        self.data = current_data
        self.feedback = feedback
        self.input = attached_input
        self.current_system = current_system
        self.attached_system = attached_system


class System:

    def __init__(self,states={},inputs={},outputs={}):
        
        #inputs have the following structure: {0:Input_object,1:Input_object,...}
        #It will be required that all the non-feedback inputs go before the feedback inputs
        #where each of the indexes is the stream of inputs. Similarly for the outputs
        #{0: Output_object, 1:Output_object,...}
        #states are just described in the states set, and the current state could only be one element of the states,
        #however one element of the states could be a vector or a higher dimension array

        compare = []
        for stream_index in inputs:
            if not inputs[stream_index].feedback:
                compare.append(stream_index)
        if compare!=np.arange(len(compare)):
            raise ValueError("all not-feedback inputs must be written after the feedback inputs")

        #sets of states behave similarly as inputs and outputs, would be: 
        #                         "RR" for any number in the real set
        #                         "II" for any integer
        #                         "CHAR" for any string
        #                         {} for any finite set of inputs // must use frozenset

        self.states = states  
        self.inputs = inputs
        self.outputs = outputs
        
        #self.states_x_inputs = product(self.states,self.inputs)
        #do we want to map all possible states_x_inputs?

        self.transition_functions = {}
        self.readout_functions = {}
        self.current_state = None
        self.states_graph = None
        self.systems = {}
        self.feedback = False

        for element in self.inputs:
            element.current_system = self
        
        for element in self.outputs:
            element.current_system = self

    def add_transition_function(self,pair, function):
        #pair is a tuple of (state,(input_object_1,..,input_object_n))
        #functions take the tuple state and data.
        #states could be single elements, arrays or arrays of arrays
        
        if pair[0] in self.states and len(pair[1]) == len(self.inputs):
            try:
                data = tuple([Input.data for Input in pair[1]])
                next_state = function((pair[0],data))
                if next_state in self.states: 
                    print("properly defined function added to transition functions")
                    self.transition_functions[pair[0]]=function
                else:
                    raise ValueError("function didn't compute valid state")
            except:
                raise Exception("function didn't compute")
        else:
            raise ValueError("either state or inputs not in states_x_inputs set")

    def add_readout_function(self,state, function):
        if state in self.states:
            try:
                output = function(state)
                found = False
                for out in self.outputs: 
                    if output in out.data: 
                        print("properly defined function added to readout functions")
                        self.readout_functions[state]=function
                        found=True
                        break
                if not found:        
                    raise ValueError("function didn't compute valid output")

            except:
                raise Exception("function didn't compute")
        else:
            raise ValueError("state not in states set")

    def get_num_nofeed(self):
        return sum([Input.feedback for Input in self.inputs])

    def transition(self,sys_input,initial_state=None):

        #sys input would be the tuple (input_object1.data,input_object2.data,...)
        #how to validate that data in inputs is correct? 
        #if its a feedback input, extract from readoutfunction and there is no need for the second 
        #element of the tuple to be used  
        if len(sys_input) == self.get_num_nofeed():
            
            if initial_state in self.states:
                self.current_state = initial_state
            elif self.current_state == None: 
                raise ValueError("can't transition without initial state")
            else:
                print("current state:",self.current_state)
                #retrieve inputs from output feedbacks 
                for stream_index in self.inputs:
                    if self.inputs[stream_index].feedback:
                        self.inputs[stream_index].data = self.readout_functions[self.current_state]
                        feedback_ = (self.inputs[stream_index].data)
                        sys_input = sys_input + feedback_
                        print("added feedback input to input data")

                    elif sys_input[stream_index] in self.inputs[stream_index].available_data:
                        self.inputs[stream_index].data = sys_input[stream_index]
                    
                    else:
                        raise ValueError("input not in input set")
                
                pair = (self.current_state,sys_input)
                self.current_state = self.transition_functions[self.current_state](pair)
                print("transitioned to state:" ,self.current_state)
                
        else:
            raise ValueError("number of inputs doesn't match number of non-feedback input streams")

    def validate_system(self):
         
        if len(self.readout_functions)>0 and len(self.transition_functions)>0:

            transition_index = list(self.transition_functions)
            edges = [(pair[0],self.transition_functions[pair](pair)) for pair in transition_index]
            self.states_graph = nx.DiGraph()
            self.states_graph.add_edges_from(edges)
            return nx.is_connected(self.states_graph)

        else:
            raise Exception("need more transition or readout functions")

    def run_experiment(self,time_steps,inputs_vector,initial_state=None):
        if validate_system():
            table = {}
            for time_step in np.arange(time_steps):
                table[time_step] = [self.current_state,inputs_vector[time_step],self.readout_functions[self.current_state]]
                self.current_state = self.transition_functions[(self.current_state,inputs_vector[time_step])]
            return table 
        else:
            raise Exception("can't run experiment without proper validation")

    def couple(self,recipes={},system2=None,new_states={},new_inputs={},new_outputs={}):
        #check recipes are properly created
        """
        four type of recipes exist, output 1 onto input 1, output 1 onto 2, output 2 onto input 2, output 2 onto input 2
        the recipes dictionary has the following shape: recipes = {(a,b):(output of system a,input of system b)}
        """
        


        #check pure feedback loops:
        for recipe in recipes:
            if recipe == (1,1):
                print("pure feedback coupling of system 1")
                if recipes[recipe][0] in self.outputs and recipes[recipe][1] in self.inputs:
                    print("updating transition function from ")
                else:
                    raise ValueError(" inputs and outputs don't match recipe")
                
                except:
                
            elif recipe == (2,2):
                print("pure feedback coupling of system 2")
            elif recipe == (1,2):
                print("output 1 onto system 2")
            elif recipe == (2,1):
                print("output 2 onto system 1")