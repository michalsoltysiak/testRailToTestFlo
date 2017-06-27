'''
Created on Jun 25, 2017

@author: slsm
'''

import csv

class SourceReader:
    h = dict()
    
    def __init__(self, fileName):
        try:
            self.csvfile = open(fileName, 'tr')
        except OSError as e:
            print( "File not found - ", fileName )
            raise e
        else:
            self.dictReader = csv.DictReader( self.csvfile )
            self.h = next( self.dictReader )
    def header(self):
        return self.h
    def nextLine(self):
        return next(self.dictReader)



if __name__ == "__main__":
    pass
