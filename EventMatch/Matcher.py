OnlineEvents = open('Windows/eventOL.txt').readlines()
OfflineEvents = open('Windows/event.txt').readlines()

index = 0
num = 0
for OLevent in OnlineEvents:
    OFFevent = OfflineEvents[index]
    if OLevent == OFFevent:
        num = num + 1
    index = index + 1

ratio = num/(index + 1)
print(ratio)