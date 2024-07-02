
import os
import subprocess
import glob
import sys
import pandas as pd
from xml.etree import ElementTree as ET
sys.path.append('../')



if __name__ == '__main__':
    ore_exe = "d:/gygCode/myORE/ore.exe"
    initialdata = "example/example15/ore.xml"
    res = subprocess.call([ore_exe, initialdata])
    
    initialdata2 = "example/example15/ore_var.xml"
    res = subprocess.call([ore_exe, initialdata2])



