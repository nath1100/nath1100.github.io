import codecs
import io
f = codecs.open("shiplist2.json", "w+", "utf-8")
with io.open("shiplist.nedb", "r", encoding='utf8') as toRead:
    r = toRead.read()
with io.open("suffix.nedb", "r", encoding='utf8') as toRead:
    s = toRead.read()
rl = r.split("\n")
length = len(rl) -1
print(length)
lineCount = 0
f.write("{")
#create dictionary for suffixes
sufDict = {}
sl = s.split("\n")
for line in sl:
    elements = line.split(",")
    #get the id
    sufId = elements[3].split(":")[1]
    romName = elements[1].split(":")[1]
    sufDict[sufId] = romName
for line in rl:
    lineList = line.split(",")
    header = lineList[0].split(":")
    # this is where it gets annoying
    idValue = header[1]
    lineList[0] = "\"id_"+ idValue + "\": {"
    #add suffix
    index = 0
    indexToEdit = 0
    changed = False
    for line in lineList:
        if line.split(":")[0] == "\"suffix\"" and line.split(":")[1]!="null}":
            searchId = line.split(":")[1].strip("}")
            romSuffix = sufDict.get(searchId)
            a = line.strip("}")+",\n\"rom_suffix\": " + romSuffix + "}"
            indexToEdit = index
            changed = True
        index +=1
    if changed:
        lineList[indexToEdit] = a  

    #dont add a , to theh last element of the line
    if lineCount != length:
        lineList[(len(lineList)-1)] += ","
    else :
        print("hit!")
    seperator = ",\n"
    trailer = seperator.join(lineList[1:])
    toWrite = lineList[0] + trailer
    f.write(toWrite)
    lineCount +=1
toWrite = "}"
f.write(toWrite)
f.close()
