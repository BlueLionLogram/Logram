from Common import regexGenerator
from Common import tokenSpliter

def dictionaryBuilder(log_format, logFile, rex):
    doubleDictionaryList = {'dictionary^DHT': -1};
    triDictionaryList = {'dictionary^DHT^triple': -1};
    allTokenList = []

    regex = regexGenerator(log_format)

    for line in open(logFile, 'r'):
        tokens = tokenSpliter(line, regex, rex)
        if(tokens == None):
            pass;
        else:
            allTokenList.append(tokens)
            for index in range(len(tokens)):
                if index >= len(tokens) - 2:
                    break;
                tripleTmp = tokens[index] + '^' + tokens[index + 1] + '^' + tokens[index + 2];
                if tripleTmp in triDictionaryList:
                    triDictionaryList[tripleTmp] = triDictionaryList[tripleTmp] + 1;
                else:
                    triDictionaryList[tripleTmp] = 1;
            for index in range(len(tokens)):
                if index == len(tokens)-1:
                    break;
                doubleTmp = tokens[index] + '^' + tokens[index+1];
                if doubleTmp in doubleDictionaryList:
                    doubleDictionaryList[doubleTmp] = doubleDictionaryList[doubleTmp] + 1;
                else:
                    doubleDictionaryList[doubleTmp] = 1;
    return doubleDictionaryList, triDictionaryList, allTokenList