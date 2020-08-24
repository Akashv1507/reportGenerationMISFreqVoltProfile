import cx_Oracle
import pandas as pd
import datetime as dt
from typing import List, Tuple


class FetchDerivedFrequency():
    """repo class to fetch derived frequency from mis_warehouse db.
    """    


    def __init__(self,con_string):
        """constructor method

        Args:
            con_string ([type]): connection string
        """        

        self.connString=con_string

    def toContextDict(self, df:pd.core.frame.DataFrame) -> dict:
        """ return derivedFrequencyDict that has two keys 1- derivedFrequencyDict['rows'] = derFreqRows
                                                         2- derivedFrequencyDict['weeklyFDI'] = weeklyFDI

        Args:
            df (pd.core.frame.DataFrame):pandas dataframe

        Returns:
            dict: derivedFrequencyDict
        """        
        
        del df['ID']
        df['DATE_KEY'] = df['DATE_KEY'].dt.day
        derFreqRows = []
        derivedFrequencyDict = {}
        weeklyFDI = (df['OUT_OF_BAND_INHRS'].sum())/168
        for ind in df.index:
            tempDict = {
                        'date' : df['DATE_KEY'][ind],
                        'max'  : df['MAXIMUM'][ind],
                        'min'  : df['MINIMUM'][ind],
                        'avg'  : df['AVERAGE'][ind],
                        'less' : df['LESS_THAN_BAND'][ind],
                        'bw'  : df['BETWEEN_BAND'][ind],
                        'great'    : df['GREATER_THAN_BAND'][ind],
                        'out'  : df['OUT_OF_BAND'][ind],
                        'outHrs': df['OUT_OF_BAND_INHRS'][ind],
                        'fdi'  : df['FDI'][ind]
                        }
            derFreqRows.append(tempDict)
        derivedFrequencyDict['rows'] = derFreqRows
        derivedFrequencyDict['weeklyFDI'] = weeklyFDI

        return derivedFrequencyDict


    def fetchDerivedFrequency(self, startDate : dt.datetime , endDate: dt.datetime)->dict:
        """fetch derived frequency from mis_warehouse db 

        Args:
            startDate (dt.datetime): start date
            endDate (dt.datetime): end date

        Returns:
            dict: return derivedFrequencyDict that has two keys 1- derivedFrequencyDict['rows'] = derFreqRows
                                                               2- derivedFrequencyDict['weeklyFDI'] = weeklyFDI
        """        
        

        try:
            connection=cx_Oracle.connect(self.connString)

        except Exception as err:
            print('error while creating a connection',err)

        else:
            print(connection.version)
            try:
                cur=connection.cursor()
                fetch_sql='''select *
                            from derived_frequency
                            where date_key between to_date(:start_date) and to_date(:end_date)'''

                cur.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD ' ")
                df=pd.read_sql(fetch_sql,params={'start_date' : startDate,'end_date': endDate},con=connection)
                         
            except Exception as err:
                print('error while creating a cursor',err)
            else:
                print('retrieval derived freq data  complete')
                connection.commit()
        finally:
            cur.close()
            connection.close()
            print("connection closed")
        derivedFrequencyDict= self.toContextDict(df)
        return derivedFrequencyDict
       
