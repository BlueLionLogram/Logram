import hashlib

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
            doubleTmp = tokens[index-1] + '^' + tokens[index]
            if doubleTmp in doubleDictionaryList and doubleDictionaryList[doubleTmp] > doubleThreshold:
                pass;
            else:
                dynamicIndex.append(index)
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
    outFile = open(outAddress + "event.txt", "w")
    templateFile = open(outAddress + "template.csv", "w")

    for tokens in allTokensList:
        indexList = tripleMatch(tokens, triDictionaryList, triThreshold)
        dynamicIndex = doubleMatch(tokens, indexList, doubleDictionaryList, doubleThreshold, len(tokens))

        logEvent = ""
        for i in range(len(tokens)):
            if i in dynamicIndex:
                tokens[i] = '<*>'
            logEvent = logEvent + tokens[i] + ' '

        if logEvent in templateTable:
            templateTable[logEvent] = templateTable[logEvent] + 1
        else:
            templateTable[logEvent] = 1

        outFile.write(logEvent);
        outFile.write('\n');

    templateFile.write('EventTemplate,Occurrences')
    templateFile.write('\n')
    for template in templateTable.keys():
        templateFile.write(template + ',' + str(templateTable[template]))
        templateFile.write('\n')