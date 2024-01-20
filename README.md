# Sysml finite state machines to Wymore finite state machine
## Introduction
The following python module is capable of receiving Sysml finite state machines in .xml format and converting to Wymorian finite state machines. 
Up to the current version, the module can only work with finite state machines that were exported from cameo Magic System of Systems software.

### Use
In the current version, the module has not been exported to pypi for remote installation so for now; all experiments have to be run locally 
and in the same folder were this repository is installed. Guide yourself from the sysml_wymore.py which has the experiments of the paper associated with the module.
In order to use the wymorian constructs and methods that allow the conversion from Sysml to Wymore systems, simply import the submethods:
```python
$ from sysml_submethods import *
```
Then, import the xml file extract the content of it and convert it to a Wymorian system in the following way:

$tree = ET.parse('yourxmlfilelocation')
$root = tree.getroot()
$regions,model_name = find_state_machine_region(root)
$states = []
$transitions = []
$activities = []
$pseudostates = []
$systems=[]
$for region in regions:
  $pseudostates,states,transitions,activities = search(region,pseudostates,states,transitions,activities)
  $pseudostates,states,transition_pairs,activities,orthogonals,fork,join,deepHistory = buildStatesTransitionsActivities(pseudostates,states,transitions,activities)
  $system = buildSystem(model_name,pseudostates,states,transition_pairs,activities,orthogonals,fork,join,deepHistory)

After creating the system object which is the Wymorian system a table of experiments can be run. In order to do so, the current state of the system has to be passed to the system object and a list of the vector of inputs.
in the following way:

$currentState = (1,0)
$inputVector = [(1,0),(0,1)]
$system.setCurrentState(currentState)
$ system.runExperiment(inputsVector=inputVector)

                
