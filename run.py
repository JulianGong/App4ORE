import os
import subprocess
import glob
import sys
import pandas as pd
from xml.etree import ElementTree as ET
sys.path.append('../')
from portfolio import Portfolios
from utility import mergeXML, MarketData

    

if __name__ == '__main__':
    
    
    ore_exe = "d:/gygCode/myORE/ore.exe"
    initialdata = "Input/0.ore.xml"
    
    res = subprocess.call([ore_exe, initialdata])
    print(res)
    