# Introduction
_testRailToTestFlo_ is a simple tool written in python (3.5+) which is created to help with importing test case definitions from _Test Rail_ to _JIRA TestFLO_.

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
                        based on section hierarhy

```


# Requirements
## System
- python 3.5 (most probably python > 3 will work as well)
- [Python JIRA](https://jira.readthedocs.io/en/master/) - `pip3 install jira`

## JIRA
- jira project with TestFLO configured / enabled
- user account with admin rights to target project (TestFLO project)

### JIRA project configuration
Basicaly you need some special configuration of the project besides having TestFLO.
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
## Data
- input file from testReail
### Supported test case types 


# Known limitations
- there is not much of error handling, so if anthing in Jira is not configured as expected the exception will be thrown
 


