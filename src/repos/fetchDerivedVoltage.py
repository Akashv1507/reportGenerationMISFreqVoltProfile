import cx_Oracle
import pandas as pd
import datetime as dt
from typing import List, Tuple, TypedDict


class FetchDerivedVoltage():
    """repo class to fetch derived voltage from mis_warehouse db.
    """

    def __init__(self, con_string):
        """constructor method

        Args:
            con_string ([type]): connection string
        """
        self.connString = con_string
        self.voltTable1 =[]
        self.voltTable2 =[]
        self.voltTable3 =[]
        self.voltTable4 =[]
        self.derivedVoltageDict ={'table1':self.voltTable1,'table2':self.voltTable2,'table3':self.voltTable3,'table4':self.voltTable4}


    def appendTables(self, df: pd.core.frame.DataFrame) -> None: 
        """ append rows for each table for each day
        voltTable1 =[]
        voltTable2 =[]
        voltTable3 =[]
        voltTable4 =[]

        Args:
            df (pd.core.frame.DataFrame): pandas dataframe that contains derived voltage data for each day for all nodes.
        """        
        date = df['DATE_KEY'][0].day

        dfTable1 = df.iloc[0:9]

        dfTable2 = df.iloc[9:18]
        dfTable2.reset_index(drop=True,inplace=True)

        dfTable3 = df.iloc[18:27]
        dfTable3.reset_index(drop=True,inplace=True)

        dfTable4 = df.iloc[27:]
        dfTable4.reset_index(drop=True,inplace=True)

        tempDictTable1 = {'date': date ,'amreliMax': round(dfTable1['MAXIMUM'][0]),'amreliMin': round(dfTable1['MINIMUM'][0]),'asojMax': round(dfTable1['MAXIMUM'][1]),'asojMin': round(dfTable1['MINIMUM'][1]),'bhilaiMax': round(dfTable1['MAXIMUM'][2]),'bhilaiMin': round(dfTable1['MINIMUM'][2]),'bhopalMax': round(dfTable1['MAXIMUM'][3]),'bhopalMin': round(dfTable1['MINIMUM'][3]),'boisarMax': round(dfTable1['MAXIMUM'][4]),'boisarMin': round(dfTable1['MINIMUM'][4]),'damohMax': round(dfTable1['MAXIMUM'][5]),'damohMin': round(dfTable1['MINIMUM'][5]),'dehgamMax': round(dfTable1['MAXIMUM'][6]),'dehgamMin': round(dfTable1['MINIMUM'][6]),'dhuleMax': round(dfTable1['MAXIMUM'][7]),'dhuleMin': round(dfTable1['MINIMUM'][7]),'gwaliorMax': round(dfTable1['MAXIMUM'][8]),'gwaliorMin': round(dfTable1['MINIMUM'][8])}
        self.voltTable1.append(tempDictTable1)
      
        tempDictTable2 = {'date': date ,'indoreMax': round(dfTable2['MAXIMUM'][0]),'indoreMin': round(dfTable2['MINIMUM'][0]),'itarsiMax': round(dfTable2['MAXIMUM'][1]),'itarsiMin': round(dfTable2['MINIMUM'][1]),'jetpurMax': round(dfTable2['MAXIMUM'][2]),'jetpurMin': round(dfTable2['MINIMUM'][2]),'kalwaMax': round(dfTable2['MAXIMUM'][3]),'kalwaMin': round(dfTable2['MINIMUM'][3]),'karadMax': round(dfTable2['MAXIMUM'][4]),'karadMin': round(dfTable2['MINIMUM'][4]),'kasorMax': round(dfTable2['MAXIMUM'][5]),'kasorMin': round(dfTable2['MINIMUM'][5]),'khandwaMax': round(dfTable2['MAXIMUM'][6]),'khandwaMin': round(dfTable2['MINIMUM'][6]),'nagdaMax': round(dfTable2['MAXIMUM'][7]),'nagdaMin': round(dfTable2['MINIMUM'][7]),'parliMax': round(dfTable2['MAXIMUM'][8]),'parliMin': round(dfTable2['MINIMUM'][8])}
        self.voltTable2.append(tempDictTable2)

        tempDictTable3 = {'date': date ,'raigarhMax': round(dfTable3['MAXIMUM'][0]),'raigarhMin': round(dfTable3['MINIMUM'][0]),'raipurMax': round(dfTable3['MAXIMUM'][1]),'raipurMin': round(dfTable3['MINIMUM'][1]),'vapiMax': round(dfTable3['MAXIMUM'][2]),'vapiMin': round(dfTable3['MINIMUM'][2]),'wardhaMax': round(dfTable3['MAXIMUM'][3]),'wardhaMin': round(dfTable3['MINIMUM'][3]),'binaMax': round(dfTable3['MAXIMUM'][4]),'binaMin': round(dfTable3['MINIMUM'][4]),'durgMax': round(dfTable3['MAXIMUM'][5]),'durgMin': round(dfTable3['MINIMUM'][5]),'gwaliorMax': round(dfTable3['MAXIMUM'][6]),'gwaliorMin': round(dfTable3['MINIMUM'][6]),'indoreMax': round(dfTable3['MAXIMUM'][7]),'indoreMin': round(dfTable3['MINIMUM'][7]),'kotraMax': round(dfTable3['MAXIMUM'][8]),'kotraMin': round(dfTable3['MINIMUM'][8])}
        self.voltTable3.append(tempDictTable3)
        
        tempDictTable4 = {'date': date ,'sasanMax': round(dfTable4['MAXIMUM'][0]),'sasanMin': round(dfTable4['MINIMUM'][0]),'satnaMax': round(dfTable4['MAXIMUM'][1]),'satnaMin': round(dfTable4['MINIMUM'][1]),'seoniMax': round(dfTable4['MAXIMUM'][2]),'seoniMin': round(dfTable4['MINIMUM'][2]),'sipatMax': round(dfTable4['MAXIMUM'][3]),'sipatMin': round(dfTable4['MINIMUM'][3]),'tamnarMax': round(dfTable4['MAXIMUM'][4]),'tamnarMin': round(dfTable4['MINIMUM'][4]),'vadodaraMax': round(dfTable4['MAXIMUM'][5]),'vadodaraMin': round(dfTable4['MINIMUM'][5]),'wardhaMax': round(dfTable4['MAXIMUM'][6]),'wardhaMin': round(dfTable4['MINIMUM'][6])}
        self.voltTable4.append(tempDictTable4)
               
            
    def fetchDerivedVoltage(self, startDate: dt.datetime, endDate: dt.datetime) :
        """fetch derived voltage from mis_warehouse db 

        Args:
            startDate (dt.datetime): start date
            endDate (dt.datetime): end date

        Returns:
            derivedVoltageDict ={'table1':voltTable1,    
                                 'table2':voltTable2,
                                 'table3':voltTable3,
                                 'table4':voltTable4
                                 }

        """

        # generating dates between startDate and endDate
        dates =[]
        delta = endDate - startDate
        for i in range(delta.days + 1):
            dates.append(startDate + dt.timedelta(days=i))
        
        try:
            connection = cx_Oracle.connect(self.connString)

        except Exception as err:
            print('error while creating a connection', err)

        else:
            print(connection.version)
            try:
                cur = connection.cursor()

                # fetching derived voltage data for each day.
                for date in dates:
                    fetch_sql = '''select  vt.mapping_id,vt.date_key, vt.node_name,mt.node_voltage, vt.maximum, vt.minimum from 
                                derived_voltage vt, voltage_mapping_table mt
                                where  vt.mapping_id = mt.id and  mt.is_included_in_daily_voltage = 'T' and date_key = to_date(:start_date)   '''

                    cur.execute(
                        "ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD ' ")
                    df = pd.read_sql(fetch_sql, params={ 'start_date': date}, con=connection)

                    #sorting node_name alphabetically.
                    df.sort_values(['NODE_VOLTAGE', 'NODE_NAME'], ascending=[True, True], inplace=True,ignore_index=True)
                    # print(df)
                    #passing object to appendTables method.
                    # df['MAXIMUM'] = df['MAXIMUM'].round().astype(int)
                    # df['MINIMUM'] = df['MINIMUM'].round().astype(int)
                    self.appendTables(df)    
                    

            except Exception as err:
                print('error while creating a cursor', err)
            else:
                print('retrieval derived voltage  data  complete')
                connection.commit()
        finally:
            cur.close()
            connection.close()
            print("connection closed")
    
        return self.derivedVoltageDict
