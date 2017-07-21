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
import json
from inspect import istraceback
from shlex import shlex
from jira.resources import IssueType





class JiraMapper:
    prioMapper = {'Medium':'Normal', 'Critical':'Critical', 'High':'High', 'Low':'Low'}
    testTypes = {'Other':'None', 'Acceptance':'Acceptance', 'Smoke':'Smoke', 'Regression':'Regression', 'Performance':'Performance', 'Development':'Development', 'Security':'Security', 'Installation':'Installation', 'Destructive':'Destructive'}
    testLevels = ['None', 'Unit', 'Integration', 'Component Interface', 'System', 'Operational Acceptance']
        
    
    def __init__(self, jiraObj, projectKey):
        '''
        :param jiraObj - initiated (created) JIRA object
        :param projectKey - string which identify project key you want to work with
        :param   
        '''
        self.errLog = ''
        self.projectKey = ''
        if isinstance(jiraObj, JIRA):
            self.jira = jiraObj
        else:
            raise JIRAError('jiraObj is not instance of JIRA class')
                     
        if isstring(projectKey):
            for p in self.jira.projects():
                if p.key == projectKey:
                    self.projectKey = projectKey
                    break
            if not self.projectKey:
                raise JIRAError(projectKey + ' is not found or user has no access')
        self.cfDict = self.__customFiledsMapping() 
        self.components = list()
        for c in self.jira.project_components(self.projectKey):
            self.components.append(c.name)
        print('Components in project: ', self.components)
        self.epics = list()
        jqlString = 'project = ' + self.projectKey + ' and issueType = Epic'
        epics = self.jira.search_issues(jqlString)
        for e in epics:
            self.epics.append({'key':e.key, 'summary':e.fields.summary, 'Epic Name':getattr(e.fields, self.cfDict['Epic Name'])})
        
    def __labelCompatybile(self, s):
        ''' returns sting in jira label-compatybile maneer - no spaces, only alphanum chars'''
        if isstring(s):
            s.strip()
            s.strip()  # remove leading and ending spaces
            s = '_'.join(s.split())  # replace spaces with _
            s = re.sub('[^0-9a-zA-Z_]+', '_', s)  # replace all non alphanum chars with _
            return s 
        else:
            return 'None'
            
    def __customFiledsMapping(self):
        
        cfMap = dict()
        meta = self.jira.createmeta(projectKeys=self.projectKey, issuetypeNames=['Test Case Template', 'Epic', 'Test Case', 'Test Plan'], expand='projects.issuetypes.fields')
        issueTypes = meta['projects'][0]['issuetypes']
        for issueType in issueTypes:
            fields = dict()
            fields = issueType['fields']
            for key in fields.keys():
                if key.find('customfield_') == 0:
                    if key in cfMap.keys():
                        print('Warning - %s is has multiple definitions in your jira' % key)
                    cfMap[fields[key]['name']] = key
                    
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
                    component = '_'.join(component.split())  # replace spaces with _
                    
                    if not component.lower() in (known.lower() for known in self.components):
                        self.jira.create_component(component, self.projectKey)
                        self.components.append(component)                        
                        print('Created component: ' + component)
                    
                    issue.fields.components.append({ 'name': component})
                issue.update(fields={'components':issue.fields.components})
            else:
                print('components argument must be sting or list of strings')
    
    def __checkAndUpdateLabels(self, issue, labels):
        if labels:
            if isstring(labels):
                l = list()
                l.append(labels)
            else:
                l = labels
            
            if type(l) is list:
                for label in l:
                    label.strip()  # remove leading and ending spaces
                    label = '_'.join(label.split())  # replace spaces with _
                            
                    if not label.lower() in (issueLabel.lower() for issueLabel in issue.fields.labels):
                        issue.fields.labels.append(label.lower())
                        issue.update(fields={'labels': issue.fields.labels})
            else:
                print(__name__ + 'labels must be string or list of strings')
    

            
    
    def __checkAndUpdateGroups(self, issue, group, subgroup=None):
        if isstring(group):
            group = self.__labelCompatybile(group)

            groups = getattr(issue.fields, self.cfDict['Test Case Group'])
            
            if groups == None:
                groups = list()
            if not group.lower() in (issueGroup.lower() for issueGroup in groups) :                
                issue.add_field_value(self.cfDict['Test Case Group'], group.lower())
        
        if not subgroup == None and isstring(subgroup):
            subgroup = self.__labelCompatybile(subgroup)
            subgroups = getattr(issue.fields, self.cfDict['Test Case Subgroup'])
            
            if subgroups == None:
                subgroups = list()
            if not subgroup.lower() in (issueSubgroup.lower() for issueSubgroup in subgroups) :                
                issue.add_field_value(self.cfDict['Test Case Subgroup'], subgroup.lower())           
            
#-------------------------------------------------------------------
    def __checkAndUpdateEpics(self, name, summary='', description=''):
        '''returns Epic's id so can be added as linked issue'''
        if summary == '':
            summary = name
        for epic in self.epics:
            if name == epic['Epic Name']:                
                return epic['key']
        
        issueDict = dict()
        issueDict['issuetype'] = {'name':'Epic'}
        issueDict['project'] = {'key': self.projectKey}
        issueDict['summary'] = summary
        issueDict[self.cfDict['Epic Name']] = name
        issueDict['description'] = description
        
        issue = self.jira.create_issue(fields=issueDict)
        self.epics.append({'key':issue.key, 'summary':issue.fields.summary, 'Epic Name':getattr(issue.fields, self.cfDict['Epic Name'])})
        print('Created epic: ', {'key':issue.key, 'summary':issue.fields.summary, 'Epic Name':getattr(issue.fields, self.cfDict['Epic Name'])})
        return issue.key
    

    def __addError(self, msg):
        if self.errLog:
            self.errLog += '\n' + msg
        else:
            self.errLog = msg
        
    def __getItem(self, trItem, trItemName):
        '''    '''
        try:
            ret = trItem[trItemName]
            return ret
        except KeyError as e:
            self.__addError('Key : "' + trItemName + '" not found in input line\n')
            

    def __getIssueFields(self, trItem):
        '''returns dictionary as jira item
        :param trItem - dictiorany object returned by sourceReader '''
        out = dict()
        description = ''
        
        sectionHierarchy = self.__getItem(trItem, 'Section Hierarchy')
        shList = re.split(' > ', sectionHierarchy)  # list of section headers
        
        # itemId = str(self.__getItem(trItem,'\ufeff"ID"'))
        itemId = str(self.__getItem(trItem, 'ID'))
        out['project'] = {'key': self.projectKey}
        out['issuetype'] = {'name':'Test Case Template'}
        
        out['summary'] =  self.__getItem(trItem, 'Title') + ' [' + itemId + ']'           
            
        try:
            out['priority'] = {'name':JiraMapper.prioMapper[self.__getItem(trItem, 'Priority')]}
        except KeyError:
            out['priority'] = {'name':'Normal'}
        
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
            s = TestSteps()
            splitExp = '.*\d\.\s+'  # each steps starts with its number
            for k, l in zip(re.split(splitExp, steps_step), re.split(splitExp, steps_expected)):
                if k or l:
                    s.add(k, '', l)  # Action, Input, Expecte result
            out[self.cfDict['Steps']] = s.asdict()
            # out[self.cfDict['Automated']] = dict({'value':'Yes'})
                
        elif template == 'Test Case (Text)':
            ''' case 2 - Given/When/Then test case  - testrail template:  Test Case (Text)'''
            ''' map to "steps" in Jira test flo '''
            s = TestSteps('Given', 'When', 'Then')
            s.add(given, when, then)
            out[self.cfDict['Steps']] = s.asdict()
            # out[self.cfDict['Automated']] = dict({'value':'Yes'})
        elif template == 'Exploratory Session':
            ''' case 3 - testrail template:  Exploratory Session'''
            s = TestSteps('Goal', 'Mission', 'Free text')
            s.add(goal, mission, '')
            out[self.cfDict['Steps']] = s.asdict()
            # commented out - does not work - Field 'customerfield_11792' cannot be set. It is not on the appropriate screen, or unknown."
            # out[self.cfDict['Automated']] = dict({'value':'No'})
            
        else:
            self.__addError('[' + itemId + '] - unknown test case template')
        
        
        # for sh, sectionText in zip(shList, list(['Section: ', 'Sub-section: ', 'Sub-sub-section: ', 'Sub-sub-sub-section: '])):
        #    description += sectionText + sh + '\n'
                
        # test type
        testType = self.__getItem(trItem, 'Type')        
        if testType in self.testTypes.keys():
            testType = self.testTypes[testType]  # translate to jira test types
            if not testType == 'None':  # you can not set type None
                out[self.cfDict['Test Type']] = list()
                out[self.cfDict['Test Type']].append({'value':testType})
            else:
                self.__addError('[%s] - did not mapped test type, type was \'Other\'' % itemId)
        elif testType == 'Automated':
            out[self.cfDict['Automated']] = dict({'value':"Yes"})
        else:
            self.__addError('[%s] - unknown test type' % itemId)
                
        description += '\n\n{quote}\n'
        description += 'Created by: ' + self.__getItem(trItem, 'Created By') + '\n'
        description += 'Created on: ' + self.__getItem(trItem, 'Created On') + '\n'
        if self.__getItem(trItem, 'Estimate'):
            description += 'Estimated for: ' + self.__getItem(trItem, 'Estimate') + '\n'
        description += '\n{quote}\n'

         
        out['description'] = description
        
        return out
    
    def createIssue(self, csvLineDict, components=None, labels=None, testLevel=None, createEpics=False):
        ''' 
        creates issue (Test Case Template) based on csvLine (from test rail export)
        returns dictrionary containing full issue definition
        :param csvLineDict - SoruceReader object 
        :param components - list of components to be assigned to created issue
        :param labels - list of labels to be assigned to created issue
        :param testLevel - value of Jira Test Level fild; allowed values are  [ 'Unit', 'Integration', 'Component Interface', 'System', 'Operational Acceptance']
        :param createEpics - enables/disables creation of Epics under which Test Case Templates are added; Epic names are detected automaticaly based on "Section Hierarchy"
        '''
        issueDict = self.__getIssueFields(csvLineDict)
        sectionHierarchy = self.__getItem(csvLineDict, 'Section Hierarchy')
        shList = re.split(' > ', sectionHierarchy)  # list of section headers
        epicName = ' / '.join(shList)
        
        if createEpics:
            print('Using epic: %s' % epicName)
            # create issue in Jira
            epicKey = self.__checkAndUpdateEpics(name=epicName, summary=sectionHierarchy, description=self.__getItem(csvLineDict, 'Section Description'))
        
            issueDict[self.cfDict['Epic Link']] = epicKey
            
        if testLevel and testLevel in self.testLevels[1:]:
            issueDict[self.cfDict['Test Level']] = dict({'value':testLevel})
        else:
            pass
            
        issue = self.jira.create_issue(fields=issueDict)        
        # append (to already created component) default labels
        self.__checkAndUpdateLabels(issue, labels)
        self.__checkAndCreateComponents(issue, components)
        if False:
            if len(shList) > 1:
                subgroup = shList[1]
            else:
                subgroup = None
                
            self.__checkAndUpdateGroups(issue, shList[1])
        
        
        return (issue.key, issue.fields.summary)
    #----------------------------------------------------------------
    def getErrors(self):
        return self.errLog
