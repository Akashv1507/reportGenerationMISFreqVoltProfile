import cx_Oracle
import pandas as pd
import datetime as dt
from typing import List, Tuple


class FetchDerivedVDI():
    """repo class to fetch derived VDI
    """    

    def __init__(self,con_string):
        """constructor method

        Args:
            con_string ([type]): connection string
        """

        self.connString=con_string
    
    def toDerivedVDIDict(self, df:pd.core.frame.DataFrame)-> dict:
        """returns derivedVDIDict that has two keys 1- derivedVDIDict['VDIRows400Kv']   =   VDIRows400Kv
                                                  2- derivedVDIDict['VDIRows765Kv']   =   VDIRows765Kv

        Args:
            df (pd.core.frame.DataFrame): pandas dataframe

        Returns:
            dict: dictionary derivedVDIDict 
        """        

        del[df['ID'],df['MAPPING_ID'],df['WEEK_START_DATE']]
        srNo = 0
        VDIRows400Kv = []
        VDIRows765Kv = []
        derivedVDIDict = {}

        group = df.groupby("NODE_VOLTAGE")
        for nameOfGroup,groupDf in group:
            
            if nameOfGroup == 400:
                for ind in groupDf.index:
                    srNo = srNo +1
                    tempDict={
                        'srNo' : srNo,
                        'name' : groupDf['NODE_NAME'][ind],
                        'max' : groupDf['MAXIMUM'][ind],
                        'min' : groupDf['MINIMUM'][ind],
                        'less': round(groupDf['LESS_THAN_BAND'][ind], 2),
                        'bet' : round(groupDf['BETWEEN_BAND'][ind], 2),
                        'great' : round(groupDf['GREATER_THAN_BAND'][ind], 2),
                        'lessHr' : round(groupDf['LESS_THAN_BAND_INHRS'][ind], 2),
                        'greatHr' : round(groupDf['GREATER_THAN_BAND_INHRS'][ind], 2),
                        'out'  : round(groupDf['OUT_OF_BAND_INHRS'][ind], 2),
                        'vdi'   : round(groupDf['VDI'][ind], 2)
                    }
                    VDIRows400Kv.append(tempDict)
            elif nameOfGroup == 765:
                for ind in groupDf.index:
                    srNo = srNo +1
                    tempDict={
                        'srNo' : srNo,
                        'name' : groupDf['NODE_NAME'][ind],
                        'max' : groupDf['MAXIMUM'][ind],
                        'min' : groupDf['MINIMUM'][ind],
                        'less': round(groupDf['LESS_THAN_BAND'][ind], 2),
                        'bet' : round(groupDf['BETWEEN_BAND'][ind], 2),
                        'great' : round(groupDf['GREATER_THAN_BAND'][ind], 2),
                        'lessHr' : round(groupDf['LESS_THAN_BAND_INHRS'][ind], 2),
                        'greatHr' : round(groupDf['GREATER_THAN_BAND_INHRS'][ind], 2),
                        'out'  : round(groupDf['OUT_OF_BAND_INHRS'][ind], 2),
                        'vdi'   : round(groupDf['VDI'][ind], 2)
                    }
                    VDIRows765Kv.append(tempDict)
        derivedVDIDict['VDIRows400Kv']   =   VDIRows400Kv
        derivedVDIDict['VDIRows765Kv']   =   VDIRows765Kv
        return derivedVDIDict




    
    def fetchDerivedVDI(self, startDate : dt.datetime )->dict:
        """fetched derived VDI from mis_warehouse db

        Args:
            startDate (dt.datetime): start-date

        Returns:
            dict: returns derivedVDIDict that has two keys 1- derivedVDIDict['VDIRows400Kv']   =   VDIRows400Kv 
                                                         2- derivedVDIDict['VDIRows765Kv']   =   VDIRows765Kv
        """        
        
        try:
            connection=cx_Oracle.connect(self.connString)

        except Exception as err:
            print('error while creating a connection',err)

        else:
            print(connection.version)
            try:
                cur=connection.cursor()
                fetch_sql='''select vdi.* from 
                            derived_vdi vdi,voltage_mapping_table mt
                            where  vdi.mapping_id = mt.id and mt.is_included_in_weekly_vdi = 'T' and week_start_date = to_date(:start_date)'''

                cur.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD' ")
                df=pd.read_sql(fetch_sql,params={'start_date' : startDate},con=connection)
                         
            except Exception as err:
                print('error while creating a cursor',err)
            else:
                print('retrieval of derived VDI data  complete')
                connection.commit()
        finally:
            cur.close()
            connection.close()
            print("connection closed")
        df['MAXIMUM'] = df['MAXIMUM'].round().astype(int)
        df['MINIMUM'] = df['MINIMUM'].round().astype(int)
        derivedVDIDict= self.toDerivedVDIDict(df)
        return derivedVDIDict
       
