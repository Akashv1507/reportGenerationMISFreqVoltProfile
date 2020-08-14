from datetime import datetime as dt
from src.appConfig import getAppConfigDict
from src. report_generation.reportGeneration import reportGeneration


configDict=getAppConfigDict()
startDate=dt.strptime("2019-07-22", '%Y-%m-%d')
endDate=dt.strptime("2019-07-28", '%Y-%m-%d')


#repo code start.

# print(freqRawTableCreator(startDate,endDate,configDict))
# print(voltageRawTableCreator(startDate,configDict))

# print(voltageDerivedTableInsertion(startDate,endDate,configDict))

# print(VDIDerivedTableInsertion(startDate,endDate,configDict))
reportGeneration(startDate,endDate,configDict)

