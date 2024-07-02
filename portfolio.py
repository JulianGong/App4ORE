# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 16:17:47 2024

@author: julia
"""

import os
import subprocess
import glob
import sys
import pandas as pd
from xml.etree import ElementTree as ET

    
        

class Portfolios(object):
    
    def __init__(self, 
        newportfolio:bool= True,
        sourcefolder = 'd:/gygCode/myORE/Meta/1.portfolio/',
        outfile = 'd:/gygCode/myORE/Input/1.portfolio.xml',
        ):
        
        self.sourcefolder = sourcefolder
        self.outfile = outfile
        
        if newportfolio:
            self.roots = ET.Element('Portfolio')
            self.roots.text = '\n\t'
        else:
            self.roots = ET.parse(self.outfile).getroot()
            
    
    def add(self, instrument, **kwargs):
        root = eval('self.%s(**kwargs)'%instrument)
        self.roots.extend(root)
        self.roots.tail = '\n'  
        ET.ElementTree(self.roots).write(self.outfile, encoding='utf-8', xml_declaration=True)
    
    def prettyNode(self, templatefile, instrument):
        file = os.path.join(self.sourcefolder, templatefile)
        root = ET.parse(file).getroot()
        for subnode in root.findall('Trade'):
            if subnode.get('id') != instrument:
                root.remove(subnode)
        
        return root
    
    def IRSNS(self, **kwargs):
        root = self.prettyNode('IRS.xml', 'IRSNS')
        
        template = root.find('Trade[@id="IRSNS"]')
        template.set('id', {'id':kwargs['tradeID']}.get('id'))
        for obj in template.findall('SwapData/LegData/Notionals/Notional'):
            obj.text = str(kwargs['Notional'])
        template.find('SwapData/LegData/FixedLegData/Rates/Rate').text = str(kwargs['Coupon'])
        for obj in template.findall('SwapData/LegData/ScheduleData/Rules/StartDate'):
            obj.text = kwargs['startD']
        for obj in template.findall('SwapData/LegData/ScheduleData/Rules/EndDate'):
            obj.text = kwargs['endD']
        return root
    
    def SwaptionNS(self,**kwargs):
        root = self.prettyNode('Swaption.xml', 'SwaptionNS')
        
        template = root.find('Trade[@id="SwaptionNS"]')
        template.set('id', {'id':kwargs['tradeID']}.get('id'))
        for obj in template.findall('SwapData/LegData/Notionals/Notional'):
            obj.text = str(kwargs['Notional'])
    
        return root
    
    
    def FXAmerican(self,**kwargs):
        root = self.prettyNode('American.xml', 'FXAmerican')
                
        template = root.find('Trade[@id="FXAmerican"]')
        template.set('id', {'id':kwargs['tradeID']}.get('id'))
        template.find('SingleAmericanOptionData/Notional').text = str(kwargs['Notional'])
        
        return root
    
    def FXAmericanNS(self,**kwargs):
        root = self.prettyNode('American.xml', 'FXAmericanNS')
                
        template = root.find('Trade[@id="FXAmericanNS"]')
        template.set('id', {'id':kwargs['tradeID']}.get('id'))
        template.find('FxOptionData/BoughtAmount').text = str(kwargs['Notional'])
        template.find('FxOptionData/SoldAmount').text = str(kwargs['Notional'])
        
        return root
    
    def FXEuropeanNS(self, **kwargs):
        root = self.prettyNode('European.xml', 'FXEuropeanNS')
                
        template = root.find('Trade[@id="FXEuropeanNS"]')
        template.set('id', {'id':kwargs['tradeID']}.get('id'))
        template.find('FxOptionData/BoughtAmount').text = str(kwargs['Notional'])
        template.find('FxOptionData/SoldAmount').text = str(kwargs['Notional'])
        return root
    
    def FXEuropean(self,**kwargs):
        root = self.prettyNode('European.xml', 'FXEuropean')
                
        template = root.find('Trade[@id="FXEuropean"]')
        template.set('id', {'id':kwargs['tradeID']}.get('id'))
        template.find('EuropeanOptionData/Notional').text = str(kwargs['Notional'])
        
        return root
    
    def FXBarrier(self,**kwargs):
        root = self.prettyNode('Barrier.xml', 'FXBarrier')
                
        template = root.find('Trade[@id="FXBarrier"]')
        template.set('id', {'id':kwargs['tradeID']}.get('id'))
        template.find('SingleBarrierOptionData/Amount').text = str(kwargs['Notional'])
        
        return root
    
    def FXAsianNS(self, **kwargs):
        root = self.prettyNode('Asian.xml', 'FXAsianNS')
                
        template = root.find('Trade[@id="FXAsianNS"]')
        template.set('id', {'id':kwargs['tradeID']}.get('id'))
        template.find('FxAsianOptionData/Quantity').text = str(kwargs['Notional'])
        
        return root 
    
    def FXAsian(self,**kwargs):
        root = self.prettyNode('Asian.xml', 'FXAsian')
                
        template = root.find('Trade[@id="FXAsian"]')
        template.set('id', {'id':kwargs['tradeID']}.get('id'))
        template.find('SingleAsianOptionData/Amount').text = str(kwargs['Notional'])
        
        return root 
    
    def RangeAccrual(self, **kwargs):
        root = self.prettyNode('RangeAccrual.xml', 'RangeAccrual')
        
        template = root.find('Trade[@id="RangeAccrual"]')
        template.set('id', {'id':kwargs['tradeID']}.get('id'))
        template.find('RangeAccrualData/Notional').text = str(kwargs['Notional'])
        
        return root 
    
    def MultipleRanges(self, **kwargs):
        root = self.prettyNode('MultipleRanges.xml', 'MultipleRanges')
        
        template = root.find('Trade[@id="MultipleRanges"]')
        template.set('id', {'id':kwargs['tradeID']}.get('id'))
        template.find('MultipleRangesData/Notional').text = str(kwargs['Notional'])
        
        return root 
    
    

if __name__ == '__main__':
    
    Portfolios(True).add('IRSNS', tradeID='Leg001', Notional =100, Coupon=0.009, startD='20160209', endD='20190209')
    Portfolios(False).add('FXAmerican',tradeID='Leg002', Notional= 2000)
    Portfolios(False).add('FXAsian',tradeID='Leg003', Notional= 2000)
    Portfolios(False).add('FXEuropean',tradeID='Leg004', Notional= 2000)
    Portfolios(False).add('MultipleRanges',tradeID='Leg005', Notional= 2000)
    
    
    
    