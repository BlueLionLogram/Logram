from DictionarySetUp import dictionaryBuilder
from MatchToken import tokenMatch
from DictionarySetUp import dictionaryBuilderTripleMap
from DictionarySetUp import dictionaryBuilderDoubleMap
from Common import regexGenerator
from Common import tokenSpliter
from Common import dictionaryTransformation
from MatchToken import tokenMatchSpark

from operator import add

HDFS_format = '<Date> <Time> <Pid> <Level> <Component>: <Content>'  # HDFS log format
Andriod_format = '<Date> <Time>  <Pid>  <Tid> <Level> <Component>: <Content>' #Andriod log format
Spark_format = '<Date> <Time> <Level> <Component>: <Content>'#Spark log format
Zookeeper_format = '<Date> <Time> - <Level>  \[<Node>:<Component>@<Id>\] - <Content>' #Zookeeper log format
Windows_format = '<Date> <Time>, <Level>                  <Component>    <Content>' #Windows log format
Thunderbird_format = '<Label> <Timestamp> <Date> <User> <Month> <Day> <Time> <Location> <Component>(\[<PID>\])?: <Content>' #Thunderbird_format
Apache_format = '\[<Time>\] \[<Level>\] <Content>' #Apache format
BGL_format = '<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>' #BGL format
Hadoop_format = '<Date> <Time> <Level> \[<Process>\] <Component>: <Content>' #Hadoop format
HPC_format = '<LogId> <Node> <Component> <State> <Time> <Flag> <Content>' #HPC format
Linux_format = '<Month> <Date> <Time> <Level> <Component>(\[<PID>\])?: <Content>' #Linux format
Mac_format = '<Month>  <Date> <Time> <User> <Component>\[<PID>\]( \(<Address>\))?: <Content>' #Mac format
OpenSSH_format = '<Date> <Day> <Time> <Component> sshd\[<Pid>\]: <Content>' #OpenSSH format
OpenStack_format = '<Logrecord> <Date> <Time> <Pid> <Level> <Component> \[<ADDR>\] <Content>' #OpenStack format
HealthApp_format = '<Time>\|<Component>\|<Pid>\|<Content>'
Proxifier_format = '\[<Time>\] <Program> - <Content>'

HDFS_Regex = [
        r'blk_(|-)[0-9]+' , # block id
        r'(/|)([0-9]+\.){3}[0-9]+(:[0-9]+|)(:|)', # IP
        r'(?<=[^A-Za-z0-9])(\-?\+?\d+)(?=[^A-Za-z0-9])|[0-9]+$', # Numbers
]
Hadoop_Regex = [r'(\d+\.){3}\d+']
Spark_Regex = [r'(\d+\.){3}\d+', r'\b[KGTM]?B\b', r'([\w-]+\.){2,}[\w-]+']
Zookeeper_Regex = [r'(/|)(\d+\.){3}\d+(:\d+)?']
BGL_Regex = [r'core\.\d+']
HPC_Regex = [r'=\d+']
Thunderbird_Regex = [r'(\d+\.){3}\d+']
Windows_Regex = [r'0x.*?\s']
Linux_Regex = [r'(\d+\.){3}\d+', r'\d{2}:\d{2}:\d{2}']
Andriod_Regex = [r'(/[\w-]+)+', r'([\w-]+\.){2,}[\w-]+', r'\b(\-?\+?\d+)\b|\b0[Xx][a-fA-F\d]+\b|\b[a-fA-F\d]{4,}\b']
Apache_Regex = [r'(\d+\.){3}\d+']
OpenSSH_Regex = [r'(\d+\.){3}\d+', r'([\w-]+\.){2,}[\w-]+']
OpenStack_Regex = [r'((\d+\.){3}\d+,?)+', r'/.+?\s', r'\d+']
Mac_Regex = [r'([\w-]+\.){2,}[\w-]+']
HealthApp_Regex = []
Proxifier_Regex = [r'<\d+\ssec', r'([\w-]+\.)+[\w-]+(:\d+)?', r'\d{2}:\d{2}(:\d{2})*', r'[KGTM]B']

from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName("log parsing").setMaster("local")
sc = SparkContext(conf=conf)

parsingLog = sc.textFile("TestLogs/HDFS_2k.log")

# counts = parsingLog.flatMap(lambda line: line.split(" ")) \
#              .map(lambda word: (word, 1)) \
#              .reduceByKey(lambda a, b: a + b)
# print(counts.collect())

# test = parsingLog.map(lambda line: line.split(" "))
# print(test.collect())

doubleList = parsingLog.flatMap(lambda line : dictionaryBuilderDoubleMap(line,HDFS_format,HDFS_Regex)) \
        .map(lambda word: (word,1)) \
        .reduceByKey(lambda a,b: a+b)
#print(doubleList.collect())
doubleKeys = doubleList.keys().collect()
doubleValues = doubleList.values().collect()
doubleDictionary = dictionaryTransformation(doubleKeys,doubleValues)
print(doubleDictionary)

tripleList = parsingLog.flatMap(lambda line : dictionaryBuilderTripleMap(line,HDFS_format,HDFS_Regex)) \
        .map(lambda word: (word,1)) \
        .reduceByKey(lambda a,b: a+b)
tripleKeys = tripleList.keys().collect()
tripleValues = tripleList.values().collect()
tripleDictionary = dictionaryTransformation(tripleKeys,tripleValues)
print(tripleDictionary)

eventList = parsingLog.map(lambda line : tokenSpliter(line,regexGenerator(HDFS_format),HDFS_Regex)) \
        .map(lambda tokens : tokenMatchSpark(tokens,doubleDictionary,tripleDictionary,15,10))