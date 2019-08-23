from Common import regexGenerator
from Common import tokenSpliter
from pyspark import SparkContext, SparkConf

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

def dictionaryBuilderDoubleMap(line, log_format, rex):
    regex = regexGenerator(log_format)
    tokenList = []
    tokens = tokenSpliter(line, regex, rex)
    if (tokens == None):
        pass;
    else:
        for index in range(len(tokens)):
            if index == len(tokens) - 1:
                break;
            doubleTmp = tokens[index] + '^' + tokens[index + 1];
            tokenList.append(doubleTmp)
    return tokenList

def dictionaryBuilderDoubleReduce():
    pass;

def dictionaryBuilderTripleMap(line, log_format, rex):
    regex = regexGenerator(log_format)
    tokens = tokenSpliter(line, regex, rex)
    tokenList = []
    if (tokens == None):
        pass;
    else:
        for index in range(len(tokens)):
            if index >= len(tokens) - 2:
                break;
            tripleTmp = tokens[index] + '^' + tokens[index + 1] + '^' + tokens[index + 2];
            tokenList.append(tripleTmp)
    return tokenList

def dictionaryBuilderTripleReduce():
    pass;