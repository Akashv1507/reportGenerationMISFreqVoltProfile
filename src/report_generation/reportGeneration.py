from src.repos.fetchDerivedFrequecny import FetchDerivedFrequency
from src.context_creator.contextCreator import ContextCreator
from src.repos.fetchDerivedVDI import FetchDerivedVDI
from src.repos.fetchDerivedVoltage import FetchDerivedVoltage
import datetime as dt
from typing import List, Tuple
from docxtpl import DocxTemplate

def reportGeneration(startDate :dt.datetime, endDate:dt.datetime, configDict: dict)-> None:
    """function that generate weekly Mis Report

    Args:
        startDate (dt.datetime): start date of weekly report
        endDate (dt.datetime): start date of weekly report
        configDict (dict): app configuration dictionary
    """    

    year = startDate.isocalendar()[0]                 
    week_number = startDate.isocalendar()[1]

    
    con_string= configDict['con_string_mis_warehouse']
    

    obj_dictMerger = ContextCreator(year, week_number, startDate, endDate)
    obj_fetchDerivedFrequency = FetchDerivedFrequency(con_string)
    obj_fetchDerivedVoltage = FetchDerivedVoltage(con_string)
    obj_fetchDerivedVDI = FetchDerivedVDI(con_string)

    
    derivedFrequencyDict = obj_fetchDerivedFrequency.fetchDerivedFrequency(startDate,endDate)
    derivedVoltageDict = obj_fetchDerivedVoltage.fetchDerivedVoltage(startDate,endDate)
    derivedVDIDict = obj_fetchDerivedVDI.fetchDerivedVDI(startDate)
    context = obj_dictMerger.contextCreator(derivedFrequencyDict['rows'], derivedFrequencyDict['weeklyFDI'],derivedVDIDict['VDIRows400Kv'],derivedVDIDict['VDIRows765Kv'],derivedVoltageDict['table1'],derivedVoltageDict['table2'],derivedVoltageDict['table3'],derivedVoltageDict['table4'])
    

    definedTemplatePath = configDict['template_path'] + '\\freq_volt_profile_raw_template.docx'
    templateSavePath = configDict['template_path'] + '\\weekly-report2.docx'
    doc = DocxTemplate(definedTemplatePath)
    doc.render(context)
    doc.save(templateSavePath)
    





