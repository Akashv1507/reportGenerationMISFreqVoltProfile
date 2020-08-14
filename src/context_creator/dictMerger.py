import datetime as dt
from typing import List, Tuple

class DictMerger():

    def __init__(self,year :int,weekNo :int, startDate: dt.datetime, endDate: dt.datetime):
        self.year=year
        self.weekNo = weekNo
        self.startDate = startDate.strftime("%Y-%m-%d")
        self.endDate =  endDate.strftime("%Y-%m-%d")
    
    def dictMerger(self,rows:List[dict],weeklyVDI:int) -> dict:
        print(round(weeklyVDI,2))
        context = {
                  'year_str' : self.year,
                  'week_no'  : self.weekNo,
                  'start_dt' : self.startDate,
                  'end_dt'   : self.endDate,
                  'weekVDI'  : round(weeklyVDI,2),
                  'derFreqList' : rows
        }
        return context