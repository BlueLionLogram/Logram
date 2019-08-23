from DictionarySetUp import dictionaryBuilder
from DictionarySetUp import dictionaryBuilderForEva
from MatchToken import tokenMatch
from MatchToken import tokenMatchForEva

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

doubleDictionaryList, triDictionaryList, allTokenList, length = dictionaryBuilder(Linux_format,
                                                                          'TestLogs/Linux.log',
                                                                          Linux_Regex)
OriginalEventList = tokenMatchForEva(allTokenList,doubleDictionaryList,triDictionaryList,15,10)
doubleDictionaryList.clear()
triDictionaryList.clear()
allTokenList.clear()

# N = length/20
# i = 1
# while N <= length:
#         doubleDictionaryList, triDictionaryList, allTokenList = dictionaryBuilderForEva(Hadoop_format,
#                                                                                   'TestLogs/Hadoop.log',
#                                                                                   Hadoop_Regex, N)
#         TestEventList = tokenMatchForEva(allTokenList, doubleDictionaryList, triDictionaryList, 15, 10)
#
#         index = 0
#         num = 0
#         for OLevent in TestEventList:
#                 OFFevent = OriginalEventList[index]
#                 if OLevent == OFFevent:
#                         num = num + 1
#                 index = index + 1
#
#         ratio = num / (index + 1)
#         N = N + (length/20)
#         doubleDictionaryList.clear()
#         triDictionaryList.clear()
#         allTokenList.clear()
#         print(str(i*5) + "%:" + str(ratio))
#         i = i + 1

N = length/20
doubleDictionaryList1, triDictionaryList1, allTokenList1 = dictionaryBuilderForEva(Linux_format,
                                                                                  'TestLogs/Linux.log',
                                                                                  Linux_Regex, N*6)
TestEventList1 = tokenMatchForEva(allTokenList1, doubleDictionaryList1, triDictionaryList1, 15, 10)

doubleDictionaryList2, triDictionaryList2, allTokenList2 = dictionaryBuilderForEva(Linux_format,
                                                                                  'TestLogs/Linux.log',
                                                                                  Linux_Regex, N*7)
TestEventList2 = tokenMatchForEva(allTokenList2, doubleDictionaryList2, triDictionaryList2, 15, 10)

index = 0
templates = []

for OLevent in TestEventList1:
    OFFevent = TestEventList2[index]
    if OLevent == OFFevent:
        pass
    else:
        if OFFevent in templates:
            pass
        else:
            templates.append(OFFevent)
    index = index + 1

for t in templates:
    print(t)

