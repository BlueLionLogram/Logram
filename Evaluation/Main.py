from DictionarySetUp import dictionaryBuilder
from MatchToken import tokenMatch
from evaluator import evaluate

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

# max = 0
# maxd = 1
# maxt = 1
#
# for t in range(1,101):
#     for d in range(t,101):
#         doubleDictionaryList, triDictionaryList, allTokenList = dictionaryBuilder(Andriod_format, 'TestLogs/Andriod_2k.log', Andriod_Regex)
#         tokenMatch(allTokenList,doubleDictionaryList,triDictionaryList,d,t,'Output/')
#         f_measure, accuracy = evaluate('GroundTruth/Andriod_2k.log_structured.csv', 'Output/event.csv')
#         if accuracy > max or max == 0:
#             max = accuracy
#             maxd = d
#             maxt = t
#         doubleDictionaryList.clear()
#         triDictionaryList.clear()
#         allTokenList.clear()
#
# print(max)
# print(maxd)
# print(maxt)

doubleDictionaryList, triDictionaryList, allTokenList = dictionaryBuilder(HealthApp_format, 'TestLogs/HealthApp_2k.log', HealthApp_Regex)
tokenMatch(allTokenList,doubleDictionaryList,triDictionaryList,15,10,'Output/HealthApp')
f_measure, accuracy = evaluate('GroundTruth/HealthApp_2k.log_structured.csv', 'Output/HealthAppEvent.csv')

#We use an automatic approach to gain the threshold. The parameters listed below are suggested thresholds for different datasets.

#Andriod: 14, 13					
#Apache: 75, 32
#BGL: 18, 10						
#HDFS: 15, 15						
#Hadoop: 9, 6						
#HPC: 13, 11						
#Linux: 32, 24						
#Mac: 11, 10						
#OpenSSH: 47, 80					
#OpenStack: 16, 9					
#Proxifier: 115, 95					
#Spark: 37, 37						
#Thunderbird: 8, 7					
#Windows: 16, 16					
#Zookeeper: 9, 9					
#HealthApp: 23, 5

