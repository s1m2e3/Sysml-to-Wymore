import xml.etree.ElementTree as ET
tree = ET.parse('State Machine (Sam).xml')
root = tree.getroot()
counter = 0
transitions = []
states = []

for child in root:
    if "Model" in child.tag:
        tag = child
        break
for child in tag:
    for element in child.attrib:
        if "Structure" in child.attrib[element]:
            print("found structure")
            structure = child
        if "Use Cases" in child.attrib[element]:
            print("found Use Cases")
            use_case = child

for child in structure:
    for element in child.attrib:
        if "State Machine" in child.attrib[element]:
            print("found System State Machine")
            ssm = child
        if "SignalEvent" in child.attrib[element]:
            print("found Transitions")
            transitions.append(child)
 
for child in ssm:
    for element in child.attrib:
        if "Region" in child.attrib[element]:
            print("found Region")
            region = child

for child in region: 
    for element in child.attrib:
        if "State" in child.attrib[element]:
            states.append(child)

print(states)
print(transitions)