'''
Created on Jun 25, 2017

@author: slsm
'''

import csv

class SourceReader:
       
    def __init__(self, fileName):
        self.h = dict()
        try:
            self.csvfile = open(fileName, 'tr')
        except OSError as e:
            print( "File not found - ", fileName )
            raise e
        else:
            self.dictReader = csv.DictReader( self.csvfile )
            self.h = self.dictReader.fieldnames
            
    def header(self):
        return self.h
    def nextLine(self):
        return next(self.dictReader)
    def __iter__(self):
        for n in self.dictReader:
            yield n

    def __del__(self):
        self.csvfile=None
        self.dictReader=None
        self.h=None

if __name__ == "__main__":
    pass
