lines = open("TestLogs/Mac.log", 'r', encoding="utf-8", errors='ignore').readlines()
outFile = open("TestLogs/NewMac.log", "w")

for line in lines:
    if line.find("Jul"):
        pass
    else:
        outFile.write(line);