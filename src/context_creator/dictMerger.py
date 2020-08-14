import datetime as dt
from typing import List, Tuple

class DictMerger():

    def __init__(self,year :int,weekNo :int, startDate: dt.datetime, endDate: dt.datetime):
        self.year=year
        self.weekNo = weekNo
        self.startDate = startDate.strftime("%Y-%m-%d")
        self.endDate =  endDate.strftime("%Y-%m-%d")
    
    def dictMerger(self,rowsFreqProfile:List[dict],weeklyFDI:int,rows400Kv:List[dict], rows765Kv:List[dict]) -> dict:
       
        context = {
                  'year_str' : self.year,
                  'week_no'  : self.weekNo,
                  'start_dt' : self.startDate,
                  'end_dt'   : self.endDate,
                  'weekVDI'  : round(weeklyFDI,2),
                  'derFreqList' : rowsFreqProfile,
                  'rows400Kv' : rows400Kv,
                  'rows765Kv'  : rows765Kv
        }
        return context