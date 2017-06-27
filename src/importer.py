'''
Created on Jun 22, 2017

@author: slsm
'''
from jira import JIRA
import sys, getopt


import json
import jiraDump

from trToJiraMapper import JiraMapper
from sourceReader import SourceReader
from testSteps import TestSteps

parsedArgs=dict()


def findFieldIdByName( jiraObject, name="Summary"):
    fieldId = ""
    for f in jiraObject.fields():
        if f['name'] == name:
            fieldId = f['id']
    return fieldId 

def customFiledsMapping( jiraObject ):
    cfMap = dict()
    for f in jiraObject.fields():        
        if f['id'].find('customfield_') == 0: #id fields starts with 'customfield_'
            cfMap[f['name']]=f['id']
        
    return cfMap 


def parseCommandLine(argv):
    dictArgs=dict({'user':'','password':'','key':'','inputFile':''})
    try:
        opts, args = getopt.getopt(argv,"hu:p:k:i:",["user=","pass=","key=","ifile="])
    except getopt.GetoptError:
        print( 'main.py -u <jira_user> -p <jira_password> -k <project_key> -i <input_file>' )
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print( 'main.py -i -u <user> -p <password> -k <project_key> -i <input_file>' )
            sys.exit()
        elif opt in ("-u", "--user"):
            dictArgs['user'] = arg
        elif opt in ("-p", "--password"):
            dictArgs['password'] = arg
        elif opt in ("-k", "--key"):
            dictArgs['key'] = arg
        elif opt in ("-i", "--ifile"):
            dictArgs['inputFile'] = arg
    return dictArgs
    
if __name__ == "__main__":
    parsedArgs = parseCommandLine(sys.argv[1:])
 


jiraTest = JIRA('https://testjira.viessmann.com',basic_auth=(parsedArgs['user'], parsedArgs['password']))
#jiraWro = JIRA('http://s0013w1602.viessmann.com:8080',basic_auth=(parsedArgs['user'], parsedArgs['password']))

jira = jiraTest

#stepsFieldId = findFieldIdByName(jira, "Steps")
print( customFiledsMapping( jira)['Steps'])

ts=TestSteps(headerAction='Given', headerInput='When', headerExpected='Then')
ts.add('a','b','c')



issue_dict = {
    'project': {'key': parsedArgs['key']},
    'summary': 'New test case template from jira-python',
    'description': 'Look into this one',
    'issuetype': {'name': 'Test Case Template'},
    'priority':{'name':'Low'},    
    customFiledsMapping( jira)['Steps']:ts.asdict()
    }
'''
ts=TestSteps()
ts.add('a','b','c')
issue_dict[stepsFieldId]=ts.asdict()
issue_dict['reporter'] = {'name': 'CebP'}

new_issue = jira.create_issue(fields=issue_dict)
'''

    
cfMap = customFiledsMapping(jira )
s = SourceReader(parsedArgs['inputFile'])        
#print( s.header() )
m= JiraMapper(parsedArgs['key'],cfMap)
#m= JiraMapper('TDC',cfMap)
for i in range(1,40):
    issueDict=m.mapLine(s.nextLine()) 
    if issueDict['description'].find('h2') > -1:
        #print(issueDict)
        print(issue_dict)
        #new_issue = jira.create_issue(fields=issueDict)
        #new_issue = jira.create_issue(fields=issue_dict)
print( jiraDump.dumpIssue(jira,'SBREST-36' ) )
#new_issue = jira.create_issue(fields=issue_dict)
#print( jira.add_comment('TDC-559', '2nd comment' ) )
#new_issue = jira.create_issue(fields=issueDict)


