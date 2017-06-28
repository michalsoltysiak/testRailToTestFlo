'''
Created on Jun 26, 2017

@author: slsm
'''
from sre_compile import isstring
import datetime
import re
from testSteps import TestSteps
from jira import JIRA
from jira.exceptions import JIRAError
import string
from pyatspi import component
from inspect import istraceback




class JiraMapper:
    prioMapper={'Medium':'Normal', 'Critical':'Critical', 'High':'High', 'Low':'Low'}
    testTypes=['None', 'Acceptance', 'Smoke', 'Regression', 'Performance', 'Development', 'Security', 'Installation', 'Destructive']
    testLevels=['None', 'Unit', 'Integration', 'Component Interface', 'System', 'Operational Acceptance']
        
    
    def __init__(self, jiraObj, projectKey):
        '''
        :param jiraObj - initiated (created) JIRA object
        :param projectKey - string which identify project key you want to work with
        :param   
        '''
        self.errLog=''
        self.projectKey = ''
        if isinstance(jiraObj, JIRA):
            self.jira = jiraObj
        else:
            raise JIRAError('jiraObj is not instance of JIRA class')
        
        
        self.cfDict = self.__customFiledsMapping()
                     
        if isstring(projectKey):
            for p in self.jira.projects():
                if p.key == projectKey:
                    self.projectKey = projectKey
                    break
            if not self.projectKey:
                raise JIRAError(projectKey+ ' is not found or user has no access') 
        self.components = list()
        for c in self.jira.project_components(self.projectKey):
            self.components.append( c.name )
        print( 'Components in project: ', self.components)

            
    def __customFiledsMapping(self):
        cfMap = dict()
        for f in self.jira.fields():        
            if f['id'].find('customfield_') == 0: #id fields starts with 'customfield_'
                cfMap[f['name']]=f['id']
        return cfMap
        
    def __checkAndCreateComponents(self, issue, components):
        if components:
            if isstring(components):
                c = list()
                c.append(components)
            else:
                c = components
            if type(c) is list:
                for component in c:
                    component.strip()
                    component = '_'.join(component.split()) #replace spaces with _
                    
                    if not component.lower() in ( known.lower() for known in self.components ):
                        self.jira.create_component(component,self.projectKey)
                        self.components.append( component )                        
                        print( 'Created component: '+ component )
                    
                    issue.fields.components.append({ 'name': component})
                issue.update(fields={'components':issue.fields.components})
            else:
                print( 'components argument must be sting or list of strings')
    
    def __checkAndUpdateLabels(self,issue,labels):
        if labels:
            if isstring(labels):
                l = list()
                l.append(labels)
            else:
                l = labels
            
            if type(l) is list:
                for label in l:
                    label.strip()   #remove leading and ending spaces
                    label = '_'.join(label.split()) #replace spaces with _
                            
                    if not label.lower() in ( issueLabel.lower() for issueLabel in issue.fields.labels ):
                        issue.fields.labels.append(label.lower())
                        issue.update(fields={'labels': issue.fields.labels})
            else:
                print( __name__ + 'labels must be string or list of strings')
           

    def __addError(self, msg):
        if self.errLog:
            self.errLog += '\n'+msg
        else:
            self.errLog = msg
        
    def __getItem(self, trItem, trItemName):
        '''    '''
        try:
            ret = trItem[trItemName]
            return ret
        except KeyError as e:
            self.__addError( 'Key : "' + trItemName + '" not found in input line\n' )
            

    def __getIssueFields(self, trItem ):
        '''returns dictionary as jira item
        :param trItem - dictiorany object returned by sourceReader '''
        out = dict()
        description = ''
        
        
        
        id = str(self.__getItem(trItem,'\ufeff"ID"'))
        out['project'] = {'key': self.projectKey}
        out['issuetype'] = {'name':'Test Case Template'}
        
        out['summary'] = self.__getItem(trItem,'Title') + '[' + id + ']'           
            
        try:
            out['priority']={'name':JiraMapper.prioMapper[self.__getItem(trItem,'Priority')]}
        except KeyError:
            out['priority']={'name':'Normal'}
        
        goal = self.__getItem(trItem, 'Goals')
        mission = self.__getItem(trItem, 'Mission')
        given = self.__getItem(trItem, 'Given')
        when = self.__getItem(trItem, 'When')
        then = self.__getItem(trItem, 'Then')
        steps_step = self.__getItem(trItem, 'Steps (Step)')
        steps_expected = self.__getItem(trItem, 'Steps (Expected Result)')

        template = self.__getItem(trItem, 'Template')
        
        ''' case 1 - Given / Steps test case  - testrail template:  Test Case (Steps)'''
        ''' map to Precondition and "steps" in Jira test flo '''
        if template == 'Test Case (Steps)':            
            out[self.cfDict['Pre-conditions']] = given            
            s=TestSteps()
            splitExp='.*\d\.\s+'
            for k, l in zip( re.split(splitExp,steps_step), re.split(splitExp,steps_expected)):
                if k or l:
                    s.add(k, '', l)
            out[self.cfDict['Steps']] = s.asdict()
            
                
        elif template == 'Test Case (Text)':
            ''' case 2 - Given/When/Then test case  - testrail template:  Test Case (Text)'''
            ''' map to "steps" in Jira test flo '''
            s=TestSteps('Given', 'When','Then')
            s.add(given, when, then)
            out[self.cfDict['Steps']] = s.asdict()
            
        elif template == 'Exploratory Session':
            ''' case 3 - Given/When/Then test case  - testrail template:  Exploratory Session'''
            s=TestSteps('Goal', 'Mission','Free text')
            s.add(goal, mission, '')
            out[self.cfDict['Steps']] = s.asdict()
            
        else:
            self.__addError('[' +id + '] - unknown test case template' )
        
        description += '\n\n{quote}\n'
        description += 'Created by: ' + self.__getItem(trItem,'Created By') + '\n'
        description += 'Created on: ' + self.__getItem(trItem,'Created On') + '\n'
        if self.__getItem(trItem,'Estimate'):
            description += 'Estimated for: ' + self.__getItem(trItem,'Estimate') + '\n'
        description += '\n{quote}\n'

        out['description'] = description
        
        testType = self.__getItem(trItem,'Type')
        sectionHierarchy = self.__getItem(trItem, 'Section Hierarchy')
        shList = re.split(' > ',sectionHierarchy )
        #print( 'type: ', testType, '\nsection: ', sectionHierarchy, '\nsplit: ',re.split(' > ',sectionHierarchy))
        '''TODO: 
            1. map test types - only works for jira Wro
            2. map epics 
        '''
        return out
    
    def createIssue(self, csvLineDict, components=None, labels=None ):
        
        issueDict = self.__getIssueFields(csvLineDict)
        sectionHierarchy = self.__getItem(csvLineDict, 'Section Hierarchy')
        shList = re.split(' > ',sectionHierarchy ) #list of section headers
        
        
        
        
        
                
        #create issue in Jira
        issue = self.jira.create_issue(fields=issueDict)
        
        #append (to already created component) default labels
        
        
        
        self.__checkAndUpdateLabels(issue, labels)
        self.__checkAndCreateComponents(issue, components)
        
        
                    
        #issue.fields.labels.append(u'new_text')
        #issue.update(fields={"labels": issue.fields.labels})        
        
        return issueDict
      
       
    
if __name__ == "__main__":
    def __checkAndUpdateLabel(label):
                
        return label
    
    print('a')
    print( __checkAndUpdateLabel(' dfa ffa    fda ') )