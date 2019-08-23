import hashlib
import re

def tripleMatch(tokens, triDictionaryList, triThreshold):
    indexList = {}

    for index in range(len(tokens)):
        if index >= len(tokens) - 2:
            break
        tripleTmp = tokens[index] + '^' + tokens[index + 1] + '^' + tokens[index + 2]
        if tripleTmp in triDictionaryList and triDictionaryList[tripleTmp] >= triThreshold:
            pass
        else:
            indexList[index] = 1
            indexList[index+1] = 1
            indexList[index+2] = 1
    return list(indexList.keys())

def doubleMatch(tokens, indexList, doubleDictionaryList, doubleThreshold, length):
    dynamicIndex = []
    for i in range(len(indexList)):
        index = indexList[i]
        if index == 0:
            doubleTmp = tokens[index] + '^' + tokens[index+1]
            if doubleTmp in doubleDictionaryList and doubleDictionaryList[doubleTmp] > doubleThreshold:
                pass;
            else:
                dynamicIndex.append(index)
        elif index == length-1:
            doubleTmp1 = tokens[index-1] + '^' + tokens[index]
            doubleTmp2 = tokens[index] + '^' + tokens[0]
            if (doubleTmp1 in doubleDictionaryList and doubleDictionaryList[doubleTmp1] >= doubleThreshold) or (doubleTmp2 in doubleDictionaryList and doubleDictionaryList[doubleTmp2] >= doubleThreshold):
                pass;
            else:
                dynamicIndex.append(index);
        else:
            doubleTmp1 = tokens[index] + '^' + tokens[index+1]
            doubleTmp2 = tokens[index-1] + '^' + tokens[index]
            if (doubleTmp1 in doubleDictionaryList and doubleDictionaryList[doubleTmp1] >= doubleThreshold) or (doubleTmp2 in doubleDictionaryList and doubleDictionaryList[doubleTmp2] >= doubleThreshold):
                pass;
            else:
                dynamicIndex.append(index);
    return dynamicIndex

def tokenMatch(allTokensList, doubleDictionaryList, triDictionaryList, doubleThreshold, triThreshold, outAddress):
    templateTable = {}
    outFile = open(outAddress + "Event.csv", "w")
    templateFile = open(outAddress + "Template.csv", "w")

    outFile.write('EventId,Event')
    outFile.write('\n')

    for tokens in allTokensList:
        indexList = tripleMatch(tokens, triDictionaryList, triThreshold)
        dynamicIndex = doubleMatch(tokens, indexList, doubleDictionaryList, doubleThreshold, len(tokens))

        logEvent = ""
        for i in range(len(tokens)):
            if i in dynamicIndex:
                tokens[i] = '<*>'
            logEvent = logEvent + tokens[i] + ' '

        logEvent = re.sub(',', '', logEvent)

        if logEvent in templateTable:
            templateTable[logEvent] = templateTable[logEvent] + 1
        else:
            templateTable[logEvent] = 1

        template_id = hashlib.md5(logEvent.encode('utf-8')).hexdigest()[0:8]

        outFile.write(template_id + ',' + logEvent);
        outFile.write('\n');

    templateFile.write('EventTemplate,Occurrences')
    templateFile.write('\n')
    for template in templateTable.keys():
        templateFile.write(template + ',' + str(templateTable[template]))
        templateFile.write('\n')