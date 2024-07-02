# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 19:09:38 2024

@author: julia
"""

import os
import subprocess
import glob
import sys
import pandas as pd
from xml.etree import ElementTree as ET


class MarketData(object):
    def __init__(self, outfile= 'd:/gygCode/myORE/Input/7.market.txt'):
        self.outfile = outfile
    
    def read(self, sourcefolder, date0 = '20160205'):
        self.sourcefolder = sourcefolder
        self.date0 = date0
        
        with open(self.outfile, 'w') as f:
            f.write("#\n")
            
        xlsxfiles = glob.glob(sourcefolder +"/*.xlsx", recursive = False)
        for filename in xlsxfiles:
            workbook = pd.read_excel(filename, sheet_name=None)
            for sheet_name, sheet in workbook.items():
                if os.path.basename(filename) == 'Rate.xlsx':
                    df,instrument = self.read_Rate(sheet_name, sheet)
                elif os.path.basename(filename) == 'FX.xlsx':
                    df,instrument = self.read_FX(sheet_name, sheet) 
                elif os.path.basename(filename) == 'FXVol.xlsx':
                    df,instrument = self.read_FXVol(sheet_name, sheet)
                elif os.path.basename(filename) == 'RateVol.xlsx':
                    df,instrument = self.read_RateVol(sheet_name, sheet)
                else:
                    continue
                
                df['date'] = self.date0
                strings = df.to_string(columns=['date','strings','Value'],index=False, header=False)
                
                with open(self.outfile, 'a') as f:
                    f.write('#'+instrument + '#\n'+ strings + '\n\n')
                    
        
    def read_Rate(self, sheet_name, data):
        if sheet_name == 'Zero Rate':
            data['strings'] = 'ZERO/RATE/' + data['CCY']+ '/' + data['CurveId']+'/'+data['dc']+ '/' +data['Tenor']
        elif sheet_name == 'Deposit Rate':
            data['strings'] = 'MM/RATE/' + data['CCY']+'/'+ data['IndexName']+ '/' +data['Forward Start'] + '/' +data['Term']
        elif sheet_name == 'FRA':
            data['strings'] = 'FRA/RATE/' +data['CCY'] + '/' + data['Forward Start'] + '/' +data['Term']
        elif sheet_name == 'Swap':
            data['strings'] = 'IR_SWAP/RATE/'+data['CCY']+'/' +data['Index Name']+'/'+ data['Forward Start'] + '/' +data['Tenor']+ '/'+data['Term'] 
        elif sheet_name == 'Basis Swap':
            data['strings'] = 'BASIS_SWAP/BASIS_SPREAD/' + data['Flat tenor']+'/' +data['Tenor'] + '/' +data['CCY'] + '/' + data['Term']
        
        return data, sheet_name
        
            
    def read_FX(self, sheet_name, data):
        if sheet_name == 'FX Spot':
            data['strings'] = 'FX/RATE/'+ data['CCY Pairs']
        elif sheet_name == 'FX FWD':
            data['strings'] = 'FXFWD/RATE/' + data['CCY Pairs'] + '/' + data['Tenor']
        elif sheet_name == 'XCCY Swap':
            data['strings'] = 'CC_BASIS_SWAP/BASIS_SPREAD/'+ data['Flat CCY'] + '/'+ data['Flat Tenor']+ '/'+data['CCY']+ '/'+data['Tenor']+ '/'+data['Term']
        
        return data, sheet_name
        
    
    def read_FXVol(self, sheet_name, data):
        CCY1,CCY2 = sheet_name[:3], sheet_name[3:]
        data = pd.melt(data, id_vars=['Term'], value_vars= data.columns[1:],var_name='Delta',value_name='Value' )
        data['strings'] = 'FX_OPTION/RATE_LNVOL/'+CCY1+'/'+CCY2+'/'+data['Term'] + '/'+ data['Delta']
        return data, sheet_name
    
    def read_RateVol(self, sheet_name, data):
        CCY,IndexTenor = sheet_name[3:6], sheet_name[7:-1]
        if sheet_name[:2] == 'CF':
            data = pd.melt(data, id_vars=['Term'], value_vars= data.columns[1:],var_name='Strike',value_name='Value' )
            data[['ATM', 'Relative']] = '0'
            data.loc[data['Strike']=='ATM','ATM'] = '1'
            data.loc[data['Strike']=='ATM','Relative'] = '1'
            data.loc[data['Strike']=='ATM','Strike'] = '0'
            data['strings'] = 'CAPFLOOR/RATE_LNVOL/'+CCY+'/'+data['Term'] +'/'+IndexTenor+ '/'+data['ATM'] + '/'+ data['Relative']+'/'+ data['Strike']
        elif sheet_name[:2] == 'SW':
            data = pd.melt(data, id_vars=['Expiry'], value_vars= data.columns[1:],var_name='Term',value_name='Value' )
            data['strings']= 'SWAPTION/RATE_LNVOL/'+CCY+ '/'+data['Expiry'] +'/'+data['Term'] + '/ATM'
                
        return data, sheet_name
    

class mergeXML(object):
    def __init__(self, outfile='Input/2.script', recursive:bool = False):
        self.outfile = outfile
        self.recursive = recursive
    
    def read(self, sourcefolder, parentNode ='ScriptLibrary'):
        assert parentNode in ['ScriptLibrary','CurveConfiguration','Conventions']
        
        roots = ET.Element(parentNode)
        roots.text = '\n\t'
        files = glob.glob(sourcefolder +"/*.xml", recursive = self.recursive)
        files = [f for f in files if os.path.basename(f) not in ["_all.xml"]]
        
        for file in files:
            root = ET.parse(file).getroot()
            root.text = '\n\t\t'
            assert root.tag == parentNode
            
            if parentNode == 'CurveConfiguration':
                for element in root:
                    if roots.find(element.tag) is None:
                        tag = ET.SubElement(roots, element.tag)
                    else:
                        tag = roots.find(element.tag)
                    tag.text = '\n\t\t'
                    tag.extend(element)
                    tag.tail = '\n'
            else:
                roots.extend(root)
            roots.tail = '\n\n'    
        
        ET.ElementTree(roots).write(self.outfile, encoding='utf-8', xml_declaration=True)
        

    


if __name__ == '__main__':
    #MarketData('d:/gygCode/myORE/Input/7.market.txt').read('Meta/7.data')
    mergeXML('Input/2.script.xml').read('meta/2.script','ScriptLibrary')
    mergeXML('Input/3.curveconfig.xml').read('meta/3.curveconfig','CurveConfiguration')
    mergeXML('Input/6.convention.xml').read('meta/6.convention','Conventions')
    