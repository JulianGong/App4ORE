import os
import subprocess
import glob
import sys
import pandas as pd
from xml.etree import ElementTree as ET
sys.path.append('../')
os.chdir("d:/gygCode/myORE")
print('python enviroment:', os.path.abspath('.'))

    

if __name__ == '__main__':
    
    ore_exe = "d:/gygCode/myORE/ore.exe"
    initialdata = "example/example2/ore.xml"
    
    #res = subprocess.call([ore_exe, initialdata])
    root = ET.parse(initialdata).getroot()
    obj_port = root.find('Setup/Parameter[@name ="portfolioFile" ]')
    obj_port.text = 'portfolio_swap.xml'
    
    
    
    
    initialdata1 = "example/example2/ore1.xml"
    ET.ElementTree(root).write(initialdata1, encoding='utf-8', xml_declaration=True)