from datetime import datetime as dt
from src.appConfig import getAppConfigDict
from src. report_generation.reportGeneration import reportGeneration


configDict=getAppConfigDict()
startDate=dt.strptime("2020-07-06", '%Y-%m-%d')
endDate=dt.strptime("2020-07-12", '%Y-%m-%d')



reportGeneration(startDate,endDate,configDict)

