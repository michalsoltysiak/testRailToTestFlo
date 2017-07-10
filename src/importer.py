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
    dictArgs=dict({'user':'','password':'','key':'','inputFile':''})
    try:
        opts, args = getopt.getopt(argv,"hu:p:k:i:s:",["user=","pass=","key=","ifile=","server="])
    except getopt.GetoptError:
        print( 'main.py -u <jira_user> -p <jira_password> -k <project_key> -i <input_file> -s <server_url>' )
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

    
     
 
if False:
    jiraWro = JIRA('http://s0013w1602.viessmann.com:8080',basic_auth=(parsedArgs['user'], parsedArgs['password']))
    
    jira = jiraWro
    cfMap = customFiledsMapping(jira )
    issueDict ={'project':{'key':'TDC'},'priority': {'name': 'Critical'}, 'issuetype': {'name': 'Test Case Template'},'summary': 'TC','components': [{ 'name': 'Documentation'}],
                cfMap['Test Type']:[{'value':'Acceptance'} ], cfMap['Test Level']:{'value':'Unit'}, cfMap['Epic Link']:'TDC-562',  
                }
    print( jiraDump.dumpIssue(jira, 'TDC-555'))
    issue = jira.issue('TDC-555')
    issue.fields.labels.append(u'new_text')

    #print( cfMap)
    #issue = jira.create_issue(fields=issueDict)
    #issue.update(labels=['imported'])
    #issue.update(notify=False, description='Quiet summary update.')
    #jira.create_component('Trigger modes', 'TDC')


if False:
    jiraTest = JIRA('https://testjira.viessmann.com',basic_auth=(parsedArgs['user'], parsedArgs['password']))
    #jiraWro = JIRA('http://s0013w1602.viessmann.com:8080',basic_auth=(parsedArgs['user'], parsedArgs['password']))
    
    jira = jiraTest
    
    cf= dict({'Fix Build': 'customfield_11699', 'Priority Value': 'customfield_12095', 'Werksauftrag': 'customfield_10060', 'EC Project': 'customfield_12090', 'Unterschiede zum Vorgänger': 'customfield_10062', 'Steps to Reproduce': 'customfield_12092', 'Ideen-Ticket': 'customfield_10391', 'Flagged': 'customfield_11190', 'Customer Journey Phase': 'customfield_11991', 'TP Progress': 'customfield_11499', 'Epic Colour': 'customfield_10695', 'Date of First Response': 'customfield_10031', 'Affected Build': 'customfield_11698', 'Wiki Link': 'customfield_10190', 'Actual Start': 'customfield_11501', 'So that': 'customfield_12000', 'Requirement': 'customfield_11694', 'CF link to Test Case Template': 'customfield_11790', 'Rough estimate (weeks):': 'customfield_12097', 'DS Zip File Version': 'customfield_10070', 'Dependencies': 'customfield_11604', 'MS-Project ID': 'customfield_11514', 'Kontext': 'customfield_11091', 'Zelle': 'customfield_11090', 'Participants': 'customfield_11900', 'Project': 'customfield_11600', 'I want to': 'customfield_11997', 'State': 'customfield_11791', 'Risks': 'customfield_11908', 'Gemeldet von': 'customfield_10081', 'Success Factors': 'customfield_11995', 'Baseline Start': 'customfield_11508', 'Actual End': 'customfield_11502', 'As a user': 'customfield_11996', 'Original estmation': 'customfield_11700', 'Cluster/Server': 'customfield_11092', 'Release Version History': 'customfield_10794', 'Automated': 'customfield_11701', 'Expected Result': 'customfield_12091', 'Watchers': 'customfield_11603', 'Requirement Level': 'customfield_11515', 'Aktivierungszeitpunkt': 'customfield_11093', 'Baseline Effort': 'customfield_11511', 'TC managers': 'customfield_11599', 'Gantt Options': 'customfield_11507', 'Referenznummer': 'customfield_10082', 'TCT Change Alert': 'customfield_11492', 'TC Status': 'customfield_11498', 'Remove Test Cases': 'customfield_11695', 'As a': 'customfield_11999', 'Status Comment': 'customfield_11909', 'TC Group': 'customfield_11491', 'Management Info': 'customfield_10083', 'Accountable': 'customfield_11903', 'Sprint': 'customfield_10690', 'Latest Start': 'customfield_11505', 'TCT managers': 'customfield_11598', 'Aha! Reference': 'customfield_11390', 'Acceptance Criteria': 'customfield_11693', 'Position': 'customfield_11901', 'Product Version': 'customfield_12096', 'Epic Name': 'customfield_10694', 'Defects on TP': 'customfield_11496', 'Story Points': 'customfield_10792', 'Defects': 'customfield_11495', 'Phase': 'customfield_12093', 'Epic/Thema': 'customfield_10791', 'Need Statement': 'customfield_11993', 'Epic Link': 'customfield_10691', 'PMR': 'customfield_11094', 'Date of Baselining': 'customfield_11510', 'Due date': 'customfield_12094', 'Testebene': 'customfield_11697', 'Markiert': 'customfield_11998', 'Precondition': 'customfield_11994', 'Visda-Ticket': 'customfield_10390', 'Gantt Chart': 'customfield_11513', 'Time in Status': 'customfield_10590', 'Planned End': 'customfield_11504', 'Plan Erledigungsdatum': 'customfield_10010', 'Latest End': 'customfield_11506', 'Change': 'customfield_11095', 'Epic Status': 'customfield_10693', 'Time': 'customfield_11905', 'Testart': 'customfield_11696', 'Cost': 'customfield_11906', 'Planned Start': 'customfield_11503', 'Business Value': 'customfield_11602', 'TC Template': 'customfield_11493', 'Rank (Obsolete)': 'customfield_10692', 'Complexity': 'customfield_11605', 'Persona': 'customfield_11992', 'Velocity %': 'customfield_11512', 'Steps': 'customfield_11497', 'System': 'customfield_10000', 'Pre-conditions': 'customfield_11691', 'issueFunction': 'customfield_10490', 'TP Status': 'customfield_11494', 'Expected': 'customfield_11904', 'Projekt ID': 'customfield_10061', 'Rank': 'customfield_11290', 'Estrella Enviroment': 'customfield_11601', 'Quality': 'customfield_11907', 'Resubmission': 'customfield_11902', 'Baseline End': 'customfield_11509', 'Geschäftswert': 'customfield_10793', 'Stakeholder': 'customfield_11990'})
    
    cfMap = customFiledsMapping(jira )
    s = SourceReader(parsedArgs['inputFile'])        
    i=0
    for l in s:
        i+=1
        m= JiraMapper(parsedArgs['key'],cfMap)
        issueDict=m.mapLine(l)
        m=None
        print(issueDict)

if False:
    cfMap= dict({'Fix Build': 'customfield_11699', 'Priority Value': 'customfield_12095', 'Werksauftrag': 'customfield_10060', 'EC Project': 'customfield_12090', 'Unterschiede zum Vorgänger': 'customfield_10062', 'Steps to Reproduce': 'customfield_12092', 'Ideen-Ticket': 'customfield_10391', 'Flagged': 'customfield_11190', 'Customer Journey Phase': 'customfield_11991', 'TP Progress': 'customfield_11499', 'Epic Colour': 'customfield_10695', 'Date of First Response': 'customfield_10031', 'Affected Build': 'customfield_11698', 'Wiki Link': 'customfield_10190', 'Actual Start': 'customfield_11501', 'So that': 'customfield_12000', 'Requirement': 'customfield_11694', 'CF link to Test Case Template': 'customfield_11790', 'Rough estimate (weeks):': 'customfield_12097', 'DS Zip File Version': 'customfield_10070', 'Dependencies': 'customfield_11604', 'MS-Project ID': 'customfield_11514', 'Kontext': 'customfield_11091', 'Zelle': 'customfield_11090', 'Participants': 'customfield_11900', 'Project': 'customfield_11600', 'I want to': 'customfield_11997', 'State': 'customfield_11791', 'Risks': 'customfield_11908', 'Gemeldet von': 'customfield_10081', 'Success Factors': 'customfield_11995', 'Baseline Start': 'customfield_11508', 'Actual End': 'customfield_11502', 'As a user': 'customfield_11996', 'Original estmation': 'customfield_11700', 'Cluster/Server': 'customfield_11092', 'Release Version History': 'customfield_10794', 'Automated': 'customfield_11701', 'Expected Result': 'customfield_12091', 'Watchers': 'customfield_11603', 'Requirement Level': 'customfield_11515', 'Aktivierungszeitpunkt': 'customfield_11093', 'Baseline Effort': 'customfield_11511', 'TC managers': 'customfield_11599', 'Gantt Options': 'customfield_11507', 'Referenznummer': 'customfield_10082', 'TCT Change Alert': 'customfield_11492', 'TC Status': 'customfield_11498', 'Remove Test Cases': 'customfield_11695', 'As a': 'customfield_11999', 'Status Comment': 'customfield_11909', 'TC Group': 'customfield_11491', 'Management Info': 'customfield_10083', 'Accountable': 'customfield_11903', 'Sprint': 'customfield_10690', 'Latest Start': 'customfield_11505', 'TCT managers': 'customfield_11598', 'Aha! Reference': 'customfield_11390', 'Acceptance Criteria': 'customfield_11693', 'Position': 'customfield_11901', 'Product Version': 'customfield_12096', 'Epic Name': 'customfield_10694', 'Defects on TP': 'customfield_11496', 'Story Points': 'customfield_10792', 'Defects': 'customfield_11495', 'Phase': 'customfield_12093', 'Epic/Thema': 'customfield_10791', 'Need Statement': 'customfield_11993', 'Epic Link': 'customfield_10691', 'PMR': 'customfield_11094', 'Date of Baselining': 'customfield_11510', 'Due date': 'customfield_12094', 'Testebene': 'customfield_11697', 'Markiert': 'customfield_11998', 'Precondition': 'customfield_11994', 'Visda-Ticket': 'customfield_10390', 'Gantt Chart': 'customfield_11513', 'Time in Status': 'customfield_10590', 'Planned End': 'customfield_11504', 'Plan Erledigungsdatum': 'customfield_10010', 'Latest End': 'customfield_11506', 'Change': 'customfield_11095', 'Epic Status': 'customfield_10693', 'Time': 'customfield_11905', 'Testart': 'customfield_11696', 'Cost': 'customfield_11906', 'Planned Start': 'customfield_11503', 'Business Value': 'customfield_11602', 'TC Template': 'customfield_11493', 'Rank (Obsolete)': 'customfield_10692', 'Complexity': 'customfield_11605', 'Persona': 'customfield_11992', 'Velocity %': 'customfield_11512', 'Steps': 'customfield_11497', 'System': 'customfield_10000', 'Pre-conditions': 'customfield_11691', 'issueFunction': 'customfield_10490', 'TP Status': 'customfield_11494', 'Expected': 'customfield_11904', 'Projekt ID': 'customfield_10061', 'Rank': 'customfield_11290', 'Estrella Enviroment': 'customfield_11601', 'Quality': 'customfield_11907', 'Resubmission': 'customfield_11902', 'Baseline End': 'customfield_11509', 'Geschäftswert': 'customfield_10793', 'Stakeholder': 'customfield_11990'})
    s = SourceReader(parsedArgs['inputFile'])        
    
    for l in s:
    
        m= JiraMapper(parsedArgs['key'],cfMap)
        issueDict=m.mapLine(l)

        print(issueDict)




    
    #new_issue = jira.create_issue(fields=issueDict)
        #new_issue = jira.create_issue(fields=issue_dict)
#print( jiraDump.dumpIssue(jira,'SBREST-36' ) )
#new_issue = jira.create_issue(fields=issue_dict)
#print( jira.add_comment('TDC-559', '2nd comment' ) )
#new_issue = jira.create_issue(fields=issueDict)


