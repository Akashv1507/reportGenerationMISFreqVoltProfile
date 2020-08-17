import datetime as dt
from typing import List, Tuple

class ContextCreator():
    """class that creates context for template 
    """    

    def __init__(self,year :int,weekNo :int, startDate: dt.datetime, endDate: dt.datetime):
        """constructor method

        Args:
            year (int): year
            weekNo (int): week no
            startDate (dt.datetime): start date
            endDate (dt.datetime): end date
        """        
        self.year=year
        self.weekNo = weekNo
        self.startDate = startDate.strftime("%Y-%m-%d")
        self.endDate =  endDate.strftime("%Y-%m-%d")
    
    def contextCreator(self,rowsFreqProfile:List[dict],weeklyFDI:int,rows400Kv:List[dict], rows765Kv:List[dict]) -> dict:
        """create context for template

        Args:
            rowsFreqProfile (List[dict]): rows in form of dictionary 
            weeklyFDI (int): weekly FDI
            rows400Kv (List[dict]): rows that belongs to 400Kv nodes
            rows765Kv (List[dict]): rows that belongs to 765Kv nodes

        Returns:
            dict: context dictionary that we render in template
        """        
       
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