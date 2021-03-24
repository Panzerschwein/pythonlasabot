import ast
import os
import random
import string

def datePretty(date):
    cTime = str(date)
    cYear = str(cTime[:4])
    cMonth = str(cTime[5:7])
    cDay = str(cTime[8:10])
    prettyDate = cMonth + "-" + cDay + "-" + cYear
    return prettyDate

def handleFile(filename):
    size = os.path.getsize(filename)
    if size == 0:
        dictionary = {}
    else:
        newFile = open(filename, 'r')
        strFile = newFile.read().strip()
        dictionary = ast.literal_eval(strFile)
        newFile.close()
    return dictionary

def editFile(filename, edit):
    file = open(filename, 'w')
    file.write(str(edit))
    file.close()

def generateID():
    letters_and_digits = string.ascii_letters + string.digits
    listCodes = handleFile('uniquecodes.txt')
    isNew = True
    done = False
    while not done:
        result_str = ''.join((random.choice(letters_and_digits) for i in range(10)))
        for i in listCodes:
            if str(i) == str(result_str):
                isNew = False
        if isNew is True:
            done = True
    listCodes.append(result_str)
    editFile('uniquecodes.txt', listCodes)
    return result_str
