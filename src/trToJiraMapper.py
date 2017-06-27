'''
Created on Jun 26, 2017

@author: slsm
'''
from sre_compile import isstring
import datetime
import re
from testSteps import TestSteps




class JiraMapper:
    prioMapper={'Medium':'Normal', 'Critical':'Critical', 'High':'High', 'Low':'Low'}
        
    def __init__(self, projectKey, customerFieldDict):
        self.errLog=''
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
            

    def mapLine(self, trItem ):
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
            del s
                
        elif template == 'Test Case (Text)':
            ''' case 2 - Given/When/Then test case  - testrail template:  Test Case (Text)'''
            ''' map to "steps" in Jira test flo '''
            s=TestSteps('Given', 'When','Then')
            s.add(given, when, then)
            out[self.cfDict['Steps']] = s.asdict()
            del s
        elif template == 'Exploratory Session':
            ''' case 3 - Given/When/Then test case  - testrail template:  Exploratory Session'''
            s=TestSteps('Goal', 'Mission','Free text')
            s.add(goal, mission, '')
            out[self.cfDict['Steps']] = s.asdict()
            del s
        else:
            self.__addError('[' +id + '] - unknown test case template' )
        
        description += '\n\n{quote}\n'
        description += 'Created by: ' + self.__getItem(trItem,'Created By') + '\n'
        description += 'Created on: ' + self.__getItem(trItem,'Created On') + '\n'
        if self.__getItem(trItem,'Estimate'):
            description += 'Estimated for: ' + self.__getItem(trItem,'Estimate') + '\n'
        description += '\n{quote}\n'

        out['description'] = description

        '''TODO: 
            1. map test types - only works for jira Wro
            2. map epics 
        '''

        
        return out
    
if __name__ == "__main__":
    cf= dict({'Fix Build': 'customfield_11699', 'Priority Value': 'customfield_12095', 'Werksauftrag': 'customfield_10060', 'EC Project': 'customfield_12090', 'Unterschiede zum Vorgänger': 'customfield_10062', 'Steps to Reproduce': 'customfield_12092', 'Ideen-Ticket': 'customfield_10391', 'Flagged': 'customfield_11190', 'Customer Journey Phase': 'customfield_11991', 'TP Progress': 'customfield_11499', 'Epic Colour': 'customfield_10695', 'Date of First Response': 'customfield_10031', 'Affected Build': 'customfield_11698', 'Wiki Link': 'customfield_10190', 'Actual Start': 'customfield_11501', 'So that': 'customfield_12000', 'Requirement': 'customfield_11694', 'CF link to Test Case Template': 'customfield_11790', 'Rough estimate (weeks):': 'customfield_12097', 'DS Zip File Version': 'customfield_10070', 'Dependencies': 'customfield_11604', 'MS-Project ID': 'customfield_11514', 'Kontext': 'customfield_11091', 'Zelle': 'customfield_11090', 'Participants': 'customfield_11900', 'Project': 'customfield_11600', 'I want to': 'customfield_11997', 'State': 'customfield_11791', 'Risks': 'customfield_11908', 'Gemeldet von': 'customfield_10081', 'Success Factors': 'customfield_11995', 'Baseline Start': 'customfield_11508', 'Actual End': 'customfield_11502', 'As a user': 'customfield_11996', 'Original estmation': 'customfield_11700', 'Cluster/Server': 'customfield_11092', 'Release Version History': 'customfield_10794', 'Automated': 'customfield_11701', 'Expected Result': 'customfield_12091', 'Watchers': 'customfield_11603', 'Requirement Level': 'customfield_11515', 'Aktivierungszeitpunkt': 'customfield_11093', 'Baseline Effort': 'customfield_11511', 'TC managers': 'customfield_11599', 'Gantt Options': 'customfield_11507', 'Referenznummer': 'customfield_10082', 'TCT Change Alert': 'customfield_11492', 'TC Status': 'customfield_11498', 'Remove Test Cases': 'customfield_11695', 'As a': 'customfield_11999', 'Status Comment': 'customfield_11909', 'TC Group': 'customfield_11491', 'Management Info': 'customfield_10083', 'Accountable': 'customfield_11903', 'Sprint': 'customfield_10690', 'Latest Start': 'customfield_11505', 'TCT managers': 'customfield_11598', 'Aha! Reference': 'customfield_11390', 'Acceptance Criteria': 'customfield_11693', 'Position': 'customfield_11901', 'Product Version': 'customfield_12096', 'Epic Name': 'customfield_10694', 'Defects on TP': 'customfield_11496', 'Story Points': 'customfield_10792', 'Defects': 'customfield_11495', 'Phase': 'customfield_12093', 'Epic/Thema': 'customfield_10791', 'Need Statement': 'customfield_11993', 'Epic Link': 'customfield_10691', 'PMR': 'customfield_11094', 'Date of Baselining': 'customfield_11510', 'Due date': 'customfield_12094', 'Testebene': 'customfield_11697', 'Markiert': 'customfield_11998', 'Precondition': 'customfield_11994', 'Visda-Ticket': 'customfield_10390', 'Gantt Chart': 'customfield_11513', 'Time in Status': 'customfield_10590', 'Planned End': 'customfield_11504', 'Plan Erledigungsdatum': 'customfield_10010', 'Latest End': 'customfield_11506', 'Change': 'customfield_11095', 'Epic Status': 'customfield_10693', 'Time': 'customfield_11905', 'Testart': 'customfield_11696', 'Cost': 'customfield_11906', 'Planned Start': 'customfield_11503', 'Business Value': 'customfield_11602', 'TC Template': 'customfield_11493', 'Rank (Obsolete)': 'customfield_10692', 'Complexity': 'customfield_11605', 'Persona': 'customfield_11992', 'Velocity %': 'customfield_11512', 'Steps': 'customfield_11497', 'System': 'customfield_10000', 'Pre-conditions': 'customfield_11691', 'issueFunction': 'customfield_10490', 'TP Status': 'customfield_11494', 'Expected': 'customfield_11904', 'Projekt ID': 'customfield_10061', 'Rank': 'customfield_11290', 'Estrella Enviroment': 'customfield_11601', 'Quality': 'customfield_11907', 'Resubmission': 'customfield_11902', 'Baseline End': 'customfield_11509', 'Geschäftswert': 'customfield_10793', 'Stakeholder': 'customfield_11990'})
    m = JiraMapper('SBREST',cf)
    d = m.mapLine({'When': '', 'Template': 'Test Case (Text)', 'Created By': 'Klaus Wenger', 'Steps (Step)': '', 'Steps': '', 'Suite ID': 'S2', 'Section Hierarchy': 'Unit Tests > Protocol Tests', 'Title': 'Encode Disconnected Message', 'Section': 'Protocol Tests', 'Section Depth': '1', 'References': '', 'Updated By': 'Sylwia Jakubiec', 'Created On': '6/24/2016 3:48 PM', 'Goals': '', 'Then': '', 'Steps (Expected Result)': '', 'Section Description': 'Tests encoding and decoding protocol messages - protobuf + base64.', 'Estimate': '', 'Priority': 'Medium', 'Mission': '', 'Given': '', '\ufeff"ID"': 'C92', 'Updated On': '8/16/2016 2:28 PM', 'Type': 'Other', 'Forecast': '', 'Suite': 'Master'})
    #d = m.mapLine({'Estimate': '', 'Created By': 'Szymon Sobocinski', 'When': '', 'Created On': '4/25/2017 6:07 PM', 'Steps (Step)': '1. Call setDataValue for the registered data with any value.\n2. Call setDataValue for the registered data again with value that does not exceed delta.', 'Type': 'Acceptance', 'Updated By': 'Szymon Sobocinski', 'Suite': 'Master', 'Mission': '', 'Title': 'Trigger mode 2 missing "type" field', 'Section Description': '', 'Then': '', 'Forecast': '', 'Section': 'Inconsistent trigger mode definition handling', 'Section Depth': '2', '\ufeff"ID"': 'C2014', 'Suite ID': 'S2', 'Goals': '', 'Given': 'Services simulator is set to respond to DeviceList message with UpdateDataDefinitionsRequest containing at least one data with definition where "sendTrigger/mode" field is set to 2, "sendTrigger/delta", and "endianness" fields are valid, but "type" field is missing.\n[C165] DC instance is connected\n[C182] Data definitions are received', 'Section Hierarchy': 'Acceptance Tests > Trigger modes > Inconsistent trigger mode definition handling', 'Steps (Expected Result)': '1. Function returns ERROR_SUCCESS\nDataChanged message is sent immedietly and carries provided value\n2. Function returns ERROR_SUCCESS\nDataChanged message is sent immedietly and carries provided value', 'Updated On': '4/25/2017 6:18 PM', 'Steps': '1. Call setDataValue for the registered data with any value.\nExpected Result:\nFunction returns ERROR_SUCCESS\nDataChanged message is sent immedietly and carries provided value\n2. Call setDataValue for the registered data again with value that does not exceed delta.\nExpected Result:\nFunction returns ERROR_SUCCESS\nDataChanged message is sent immedietly and carries provided value', 'References': '', 'Template': 'Test Case (Steps)', 'Priority': 'High'})
    #d = m.mapLine({'Created On': '8/17/2016 4:08 PM', 'Forecast': '', 'Title': 'Verify SSL/TLS connection to the management service', 'Section Depth': '1', 'Template': 'Exploratory Session', 'Section Description': '', 'Steps (Step)': '', '\ufeff"ID"': 'C145', 'References': '', 'Priority': 'Medium', 'Goals': 'List of accepted ciphers suites should not contain weak ciphers: RC4, DES, 3DES\nTLS v1.2 should be used', 'Type': 'Other', 'Section': 'Retrieve Connection Information from Server', 'Then': '', 'Section Hierarchy': 'Acceptance Tests > Retrieve Connection Information from Server', 'Updated On': '8/30/2016 9:52 AM', 'Mission': 'Verify:\n- list of cipher suites advertised by DCe in TLS/SSL connection establishment procedure\n- SSL/TLS version', 'Suite': 'Master', 'Given': '', 'Steps (Expected Result)': '', 'Updated By': 'Szymon Sobocinski', 'Steps': '', 'When': '', 'Estimate': '', 'Suite ID': 'S2', 'Created By': 'Sylwia Jakubiec'})
    print( d)
    print('errors: ',m.errLog)

