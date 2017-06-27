'''
Created on Jun 23, 2017

@author: slsm
'''
from _ast import Num

stepHeader={'columns':[
    {'isStatus':False,'name':'Action','number':1},
    {'isStatus':False,'name':'Input','number':2},
    {'isStatus':False,'name':'Expected result','number':3},
    {'isStatus':True,'name':'Status','number':4}
    ],'number':0}
'''
stepHeader={'columns':[
    {'isStatus':False,'name':'Given','number':1},
    {'isStatus':False,'name':'When','number':2},
    {'isStatus':False,'name':'Then','number':3},
    {'isStatus':True,'name':'Status','number':4}
    ],'number':0}
'''

class Step:
    '''
    classdocs
    '''
    action=''
    input=''
    expectedResult=''
    number=0
    def __init__(self, number, actionString='', inputString='', expectedResultString=''):
        '''
        Constructor
        '''
        self.action=actionString
        self.input=inputString
        self.expectedResult=expectedResultString
        self.number=number
        
    def asdict(self):
        l = list()
        l.append(dict(
            {'groupId':0,
             'isStatus':False,
             'number':1,
             'value':self.action},
            ))
        l.append(dict(
            {'groupId':0,
             'isStatus':False,
             'number':2,
             'value':self.input},
            ))
        l.append(dict(
            {'groupId':0,
             'isStatus':False,
             'number':3,
             'value':self.expectedResult},
            ))
        l.append(dict(
            {'groupId':0,
             'isStatus':True,
             'number':4,
             'value':''},
            ))
        return l
       
    
class TestSteps():
    
    steps=list()
    header = dict()
    def __init__(self, headerAction='Action', headerInput='Input', headerExpected='Expected result'):
        self.header = stepHeader
        if headerAction or headerInput or headerExpected:            
            self.header['columns'][0]['name']=headerAction
            self.header['columns'][0]['name']=headerInput
            self.header['columns'][0]['name']=headerExpected
        
    def add(self,actionString='', inputString='', expectedResultString=''):
        self.steps.append(Step(len(self.steps)+1, actionString, inputString, expectedResultString))
    
    def clear(self):
        self.steps.clear()
    
    
        
    
    def asdict(self):
        d = dict()
        d['header']=self.header
        d['rows']=list()
        for s in self.steps:
            stepDict=s.asdict()
            d['rows'].append(dict({'columns':stepDict,'number':s.number}))
        return d
            
if __name__ == "__main__":
    pass



    