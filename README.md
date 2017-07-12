# Introduction
_testRailToTestFlo_ is a simple tool written in python (3.5+) which is created to help with importing test case definitions from _Test Rail_ to _JIRA TestFLO_.

__Important__ please look to Mapping section as the tool is designed mainly to import DCe related test cases,
you will need to branch to import other test cases

# How to use
In general the tool is command line tool.

Type `python importer.py -h` for help. 
```
usage: importer.py [-h] -s server-url -k PROJECTKEY -u username -p password -i
                   input_file.csv [-l [label [label ...]]]
                   [-c [component [component ...]]] [-e]

Transfers TestRail test cases from csv file to specified TestFLO project in
Jira.

optional arguments:
  -h, --help            show this help message and exit
  -s server-url, --server server-url
                        url of your jira server, including http(s)://
  -k PROJECTKEY, --key PROJECTKEY
                        project KEY, not name, not id, the KEY
  -u username, --user username
                        your jira user name
  -p password, --pass password
                        your jira passowrd
  -i input_file.csv, --ifile input_file.csv
                        path to source file (csv)
  -l [label [label ...]], --labels [label [label ...]]
                        space delimited list of label to be assigned to
                        imported issues
  -c [component [component ...]], --components [component [component ...]]
                        space delimited list of components to be assigned to
                        imported issues
  -e                    add if you want to enable automatic creation of epics
                        based on section hierarchy

```


# Requirements
## System
- python 3.5 (most probably python > 3 will work as well)
- [Python JIRA](https://jira.readthedocs.io/en/master/) - `pip3 install jira`

## JIRA
- jira project with TestFLO configured / enabled
- user account with admin rights to target project (TestFLO project)

### JIRA project configuration
Basically you need some special configuration of the project besides having TestFLO.

Following extra configurations are required:
1. Issue types:
	* Test Case Template
	* Test Case
	* Test Plan
	* Epic - _especially if `-e` parameter used_
2. Additional (custom) fields in Jira
	* __Test Level__ - schema as follows
		```
		 "customfield_13292": {
                            "required": false,
                            "schema": {
                                "type": "option",
                                "custom": "com.atlassian.jira.plugin.system.customfieldtypes:select",                          
                            },
                            "name": "Test Level",
                            "hasDefaultValue": false,
                            "operations": [
                                "set"
                            ],
                            "allowedValues": [
                                {                                    
                                    "value": "Unit"                                 
                                },
                                {
                                    "value": "Integration"
                                },
                                {
                                    "value": "Component Interface"
                                },
                                {
                                    "value": "System"
                                },
                                {
                                    "value": "Operational Acceptance"
                                }
                            ]
                        }
        ```      
	* __Test Type__ - schema as follows:
		```
		"customfield_13291": {
                            "required": false,
                            "schema": {
                                "type": "array",
                                "items": "option",
                                "custom": "com.atlassian.jira.plugin.system.customfieldtypes:multiselect"                                
                            },
                            "name": "Test Type",
                            "hasDefaultValue": false,
                            "operations": [
                                "add",
                                "set",
                                "remove"
                            ],
                            "allowedValues": [
                                {
                                    "value": "Acceptance"
                                },
                                {
                                    "value": "Smoke"
                                },
                                {
                                    "value": "Regression"
                                },
                                {
                                    "value": "Performance"
                                },
                                {
                                    "value": "Development"
                                },
                                {
                                    "value": "Security"
                                },
                                {
                                    "value": "Installation"
                                },
                                {
                                    "value": "Destructive"
                                }
                            ]
                        }
		```
	* __Test Case Group__ - schema:
		```
			"customfield_13293": {
                            "required": false,
                            "schema": {
                                "type": "array",
                                "items": "string",
                                "custom": "com.atlassian.jira.plugin.system.customfieldtypes:labels",
                                "customId": 13293
                            },
                            "name": "Test Case Group",
                            "hasDefaultValue": false,
                            "operations": [
                                "add",
                                "set",
                                "remove"
                            ]
                        }
		
		``` 
	* __Test Case Subgroup__ - schema:
		```
		 "customfield_13294": {
                            "required": false,
                            "schema": {
                                "type": "array",
                                "items": "string",
                                "custom": "com.atlassian.jira.plugin.system.customfieldtypes:labels",
                            },
                            "name": "Test Case Subgroup",
                            "hasDefaultValue": false,
                            "operations": [
                                "add",
                                "set",
                                "remove"
                            ]
                        }
		```
	* __Epic Link__ - schema:
		```
		 "customfield_10691": {
                            "required": false,
                            "schema": {
                                "type": "any",
                                "custom": "com.pyxis.greenhopper.jira:gh-epic-link",
                                "customId": 10691
                            },
                            "name": "Epic Link",
                            "hasDefaultValue": false,
                            "operations": [
                                "set"
                            ]
                        }
		```
	* __Pre-conditions__ - schema:
		```
		 "customfield_11590": {
                            "required": false,
                            "schema": {
                                "type": "string",
                                "custom": "com.atlassian.jira.plugin.system.customfieldtypes:textarea",
                                "customId": 11590
                            },
                            "name": "Pre-conditions",
                            "hasDefaultValue": true,
                            "operations": [
                                "set"
                            ]
                        }
		```
	* __Automated__ - schema:
		```
		"customfield_11792": {
                            "required": false,
                            "schema": {
                                "type": "option",
                                "custom": "com.atlassian.jira.plugin.system.customfieldtypes:select",
                            },
                            "name": "Automated",
                            "hasDefaultValue": true,
                            "operations": [
                                "set"
                            ],
                            "allowedValues": [
                                {
                                    "value": "Yes"
                                },
                                {
                                    "value": "No"
                                }
                            ]
                        }
		```
3. All above mentioned fields __have to__ be added to _Create issue Screen_ and _Edit Issue Screen_, otherwise you will see error msg from JIRA.
	* additionally would be nice to have them in screens where you read the issue content (default screen or _View Issue Screen_) 
	
## Data
- input file from testReail 
	- example in the repo - `example.csv`
### Supported test case types (Test Rail _Template_)
- Test Case (Steps)
- Test Case (Text)
- Exploratory Session

# Mapping
The script(s) maps Test Rails issues to TestFLO issues in a following way:
* _ID_ - added at the end of __Summary__ in square braces
* _Title_ - mapped to __Summary__
* _Created By_ - added as a part of __Description__
* _Created On_ - added as a part of __Description__
* _Estimate_ - added as a part of __Description__
* ~~_Forecast_~~ - skipped
* _Given_ 
	* in case of _Test Case (Text)_ mapped to __Steps__ with "Given", "When", "Then" headers, _Given_ filed
	* in case of _Test Case (Steps)_ mapped to __Pre-condition__ with "Given", "When", "Then" headers
* _Goals_
	* only exists in _Exploratory Session_, mapped to __Steps__  with "Goal", "Mission", "Free text" headers	 
* _Mission_
	* only exists in _Exploratory Session_, mapped to __Steps__  with "Goal", "Mission", "Free text" headers
* _Priority_ - JIRA __Priority__
* ~~_References_~~ - skipped
* ~~_Section_~~ - skipped
* ~~_Section Depth_~~ - skipped
* _Section Description_ - when using _Epics_ (`-e`) used as __Description__ of issue type _Epic_
* _Section Hierarchy_ (format looks like follows: section > subsection > subsubsection > ....)
	* in case of _DCe_ test cases 
		* first level section is mapped to __Test Type__ and __Test Level__
		* second level is mapped to __Test Case Group__ and (with `-e`) to __Epic Name__ and __Summary__ of Epic issue (parent of test case template)
		* if exists, third level is mapped to __Test Case Subgroup__ and (with `-e`) to __Epic Name__ and __Summary__ of Epic issue (parent of test case template)
* ~~_Steps_~~ - skipped
* _Steps (Expected Result)_ - mapped to _Expected result_ of __Steps__
* _Steps (Step)_  - mapped to _Action_ of __Steps__
* ~~_Suite_~~ - skipped
* ~~_Suite ID_~~ - skipped
* _Template_ - used to recognize way of mapping (Given/When/Then, Action/Expected result, Mission/Goal)
* _Then_ - in case of _Test Case (Text)_ mapped to __Steps__ with "Given", "When", "Then" headers, _Then_ filed 
* _Type_ - mapped to __Test Type__
* ~~_Updated By_~~ - skipped
* ~~_Updated On_~~ - skipped
* _When_ - in case of _Test Case (Text)_ mapped to __Steps__ with "Given", "When", "Then" headers, _When_ filed

# Known limitations
- there is not much of error handling, so if anything in Jira is not configured as expected the exception will be thrown
- tool only check duplicates of Epics and components, __does not__ check for duplicates of _Test Cases Template_ issues 
	- so if you run it second time with the seme input params you will __have all issues duplicated__ 
- Mapping of _Test Type_ and _Test Level_ is implemented as DCe-specific  
- Original Test Rail's ID is added to issue summary with square braces []



 


