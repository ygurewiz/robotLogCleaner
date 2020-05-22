import re
import string
import datetime
from pathlib import Path
import sys
import os


def robotLogCleaner(argv):

    if(len(argv)==1):
        print("Input file Directory full path:")
        inputDir = input()
        print("Input file full name")
        robotile = input()
    else:
        inputDir = os.getcwd()
        rFile = argv[1]
        
    #open input file
    try:
        filePath = inputDir+'\\'+rFile
        rFile = open(filePath,'r')
    except IOError: 
           print ("Log File: File does not appear to exist.")
           return
    outputfileName = str.replace(rFile.name,'.log','_Cleaned.log')
    outputFile = open(outputfileName,'w+')

    lines = rFile.readlines()
 
    robotLineParser(lines,outputFile)

    rFile.close()
    outputFile.close()

def robotLineParser(lines,outputFile):
    for line in lines:
        if(not re.search(r'\bLOG_SENSORS_ID_EVENT\b', line)):
            outputFile.writelines(line)
               
def main():
    robotLogCleaner(sys.argv)


if __name__=="__main__":
    main()
