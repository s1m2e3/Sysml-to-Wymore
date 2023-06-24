import xml 
import xml.etree.ElementTree as ET
#from system import *


#def sysml_to_wymore(file):
    
    


#return wymore_system 

if __name__=="__main__":
    file = "SIE558_Joanna Joseph_MA2.xml"
    tree = ET.parse(file)
    root = tree.getroot()
    for child in root:
        #print(child.attrib)
        print(child.tag)
