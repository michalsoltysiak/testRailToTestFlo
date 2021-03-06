'''
Created on Jun 22, 2017

@author: slsm
'''
from jira import JIRA
import sys



import argparse

from trToJiraMapper import JiraMapper
from sourceReader import SourceReader
from testSteps import TestSteps
from ast import parse
from builtins import str
from getpass import getpass



def findFieldIdByName(jiraObject, name="Summary"):
    fieldId = ""
    for f in jiraObject.fields():
        if f['name'] == name:
            fieldId = f['id']
    return fieldId 

def customFiledsMapping(jiraObject):
    cfMap = dict()
    for f in jiraObject.fields():        
        if f['id'].find('customfield_') == 0:  # id fields starts with 'customfield_'
            cfMap[f['name']] = f['id']
        
    return cfMap 


def parseCommandLine(argv):
    dictArgs = dict({'user':'', 'key':'', 'inputFile':'', 'server':'', 'epics':False})
    parser = argparse.ArgumentParser(description='Transfers TestRail test cases from csv file to specified TestFLO project in Jira.')
    parser.add_argument('-s', '--server', metavar='server-url', nargs=1, required=True, type=str, help='url of your jira server, including http(s)://')
    parser.add_argument('-k', '--key', metavar='PROJECTKEY', nargs=1, required=True, type=str, help='project KEY, not name, not id, the KEY')
    parser.add_argument('-u', '--user', metavar='username', nargs=1, required=True, type=str, help='your jira user name')
    parser.add_argument('-i', '--ifile', metavar='input_file.csv', nargs=1, required=True, type=str, help='path to source file (csv)')
    parser.add_argument('-l', '--labels', metavar='label', nargs='*', required=False, type=str, help='space delimited list of label to be assigned to imported issues')
    parser.add_argument('-c', '--components', metavar='component', nargs='*', required=False, type=str, help='space delimited list of components to be assigned to imported issues')
    parser.add_argument('-e', action='store_true', help='add if you want to enable automatic creation of epics based on section hierarchy')
    parser.add_argument('-t', '--level', metavar='test_level', nargs=1, required=False, type=str,
                        help='Test level to be set for each of imported issues, one of: Unit, Integration, "Component Interface", System, "Operational Acceptance"')
    args = vars(parser.parse_args())
    dictArgs['user'] = args['user'][0]
    dictArgs['key'] = args['key'][0]
    dictArgs['inputFile'] = args['ifile'][0]
    dictArgs['server'] = args['server'][0]
    dictArgs['epics'] = args['e']
    dictArgs['labels'] = args['labels']
    dictArgs['components'] = args['components']
    if args['level'] and type(args['level']) is list and len(args['level'])>0:
        dictArgs['level'] = args['level'][0]
    else:
        dictArgs['level'] = None
    return dictArgs
if __name__ == "__main__":
    parsedArgs = parseCommandLine(sys.argv[1:])

else:
    pass
 
 
if True:
    jiraPass = getpass("Please enter your JIRA password: ")
    jira = JIRA(parsedArgs['server'], basic_auth=(parsedArgs['user'], jiraPass))
    m = JiraMapper(jira, parsedArgs['key'])
    s = SourceReader(parsedArgs['inputFile'])
    i = 0
    for csvLine in s:
        i = i + 1
        print('created issue: %s - %s' % m.createIssue(csvLine, 
                                                       components=parsedArgs['components'], 
                                                       labels=parsedArgs['labels'], 
                                                       createEpics=parsedArgs['epics'], 
                                                       testLevel=parsedArgs['level'] ))
    print( '\nError log: \n%s' % m.getErrors() )
    

