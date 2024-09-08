import datetime as dt  
def isNowAfter(startTime): 
        nowTime = dt.datetime.now().time()
        #Over midnight: 
        return nowTime >= startTime 

#normal example: 
print(isNowAfter(dt.time(13,10)))

#over midnight example: 
print(isNowAfter(dt.time(20,30)))

startTimeRunAll = "14:20"
if startTimeRunAll != "":
    starthour = int(startTimeRunAll.split(":")[0])
    startmin = int(startTimeRunAll.split(":")[1])
    if isNowAfter(dt.time(starthour,startmin)):
        print("Running all tests as we are after " + startTimeRunAll)
        testtypes = []
        runningallday = True


vstestlocation = ""
if vstestlocation.endswith('"'):
    vstestlocation = vstestlocation[:-1]
if not vstestlocation.endswith("\\"):
    if vstestlocation != "":
        vstestlocation = vstestlocation + "\\"
vstestlocation = '"' + vstestlocation + 'vstest.console"'
if vstestlocation == '"vstest.console"':
    vstestlocation = "vstest.console"
print(vstestlocation)