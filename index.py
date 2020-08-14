from datetime import datetime as dt
from src.appConfig import getAppConfigDict
from src. report_generation.reportGeneration import reportGeneration


configDict=getAppConfigDict()
startDate=dt.strptime("2019-07-22", '%Y-%m-%d')
endDate=dt.strptime("2019-07-28", '%Y-%m-%d')



reportGeneration(startDate,endDate,configDict)

