'''
Created on Jun 26, 2017

@author: slsm
'''
from sre_compile import isstring
from lxml.html._diffcommand import description

prioMapper={'Medium':'Normal', 'Critical':'Critical', 'High':'High', 'Low':'Low'}

class JiraMapper:
    errMsg=''
    errLog=''
    
    def __init__(self, projectKey, customerFieldDict):
        if isinstance(customerFieldDict, dict):
            self.cfDict = customerFieldDict
        else:
            self.cfDict = dict()
            print('Warning: are you sure you dont\'n  have custom fileds?' )
             
        if isstring(projectKey):
            self.projectKey = projectKey
        else:
            self.projectKey = 'WRONG-KEY'
            print('projectKey must be a string')

    
    def __getItem(self, trItem, trItemName):
        '''    '''
        try:
            ret = trItem[trItemName]
            return ret
        except KeyError as e:
            self.errLog += 'Key : "' + trItemName + '" not found in input line\n'
            

    def mapLine(self, trItem ):
        '''returns dictionary as jira item
        :param trItem - dictiorany object returned by sourceReader '''
        out = dict()
        description = ''
        mission=''
        
        out['project'] = {'key': self.projectKey}
        out['issuetype'] = {'name':'Test Case Template'}
        
        out['summary'] = self.__getItem(trItem,'Title')           
            
        try:
            out['priority']={'name':prioMapper[self.__getItem(trItem,'Priority')]}
        except KeyError:
            out['priority']={'name':'Normal'}
        
        #map Goals and Mission to h2. sections in Description
        goal = self.__getItem(trItem, 'Goals')
        if goal:
            description = 'h2. Goals\n'
            description += goal
        mission = self.__getItem(trItem, 'Mission')
        if mission:
            description += '\n\nh2. Mission\n'
            description += mission
        

        #precondition
        try:
            out[self.cfDict['Pre-conditions']] = self.__getItem(trItem,'Given')            
        except KeyError as e:
            self.errMsg='Key error '
    
        if False: 
            out['created']=self.__getItem(trItem,'Created On')
            out['timeestimate']=self.__getItem(trItem,'Estimate')
            out['reporter']={'name': self.__getItem(trItem,'Created By')}
        else:
            description += '\n\n{quote}\n'
            description += 'Created by: ' + self.__getItem(trItem,'Created By') + '\n'
            description += 'Created on: ' + self.__getItem(trItem,'Created On') + '\n'
            if self.__getItem(trItem,'Estimate'):
                description += 'Estimated for: ' + self.__getItem(trItem,'Estimate') + '\n'
            description += '\n{quote}\n'
    
    
        out['description'] = description
        
        return out
    
if __name__ == "__main__":
    cf= dict({'a':'b'})
    m = JiraMapper('SBREST',cf)
    d = m.mapLine({'Title':'title'})
    print( d)
    print(m.errLog)

