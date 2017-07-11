'''
Created on Jun 22, 2017

@author: slsm
'''
from jira import JIRA
import sys, getopt


import json


from trToJiraMapper import JiraMapper
from sourceReader import SourceReader
from testSteps import TestSteps



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
    dictArgs=dict({'user':'','password':'','key':'','inputFile':'', 'server':''})
    try:
        opts, args = getopt.getopt(argv,"hu:p:k:i:s:",["user=","pass=","key=","ifile=","server="])
    except getopt.GetoptError:
        print( 'importer.py -u <jira_user> -p <jira_password> -k <project_key> -i <input_file> -s <server_url>' )
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print( 'main.py -i -u <user> -p <password> -k <project_key> -i <input_file> -s <server_url>' )
            sys.exit()
        elif opt in ("-u", "--user"):
            dictArgs['user'] = arg
        elif opt in ("-p", "--password"):
            dictArgs['password'] = arg
        elif opt in ("-k", "--key"):
            dictArgs['key'] = arg
        elif opt in ("-i", "--ifile"):
            dictArgs['inputFile'] = arg
        elif opt in ("-s", "--server"):
            dictArgs['server'] = arg
    return dictArgs

parsedArgs = dict()    
if __name__ == "__main__":
    parsedArgs = parseCommandLine(sys.argv[1:])
 
 
 
if True:
    jiraTest = JIRA(parsedArgs['server'],basic_auth=(parsedArgs['user'], parsedArgs['password']))

    out = jiraTest.createmeta(projectKeys=parsedArgs['key'], issuetypeNames=['Test Case Template','Epic'], expand='projects.issuetypes.fields')
#    p= out['projects'][0]['issuetypes'][0]['fields']
    
    
    m=JiraMapper(jiraTest, parsedArgs['key'])
    s = SourceReader(parsedArgs['inputFile'])
    #print( m.cfDict )  
    
    for csvLine in s:
        print( m.createIssue(csvLine, ['DCe'], 'imported'  ) )

    
     


