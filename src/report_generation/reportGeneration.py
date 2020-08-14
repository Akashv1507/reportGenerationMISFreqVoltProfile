from src.repos.fetchDerivedFrequecny import FetchDerivedFrequency
from src.context_creator.dictMerger import DictMerger
from src.repos.fetchDerivedVDI import FetchDerivedVDI
import datetime as dt
from typing import List, Tuple
from docxtpl import DocxTemplate

def reportGeneration(startDate :dt.datetime, endDate:dt.datetime, configDict: dict)-> None:

    year = startDate.isocalendar()[0]
    week_number = startDate.isocalendar()[1]

    
    con_string= configDict['con_string_local']
    

    obj_dictMerger = DictMerger(year, week_number, startDate, endDate)
    obj_fetchDerivedFrequency = FetchDerivedFrequency(con_string)
    obj_fetchDerivedVDI = FetchDerivedVDI(con_string)

    


    derivedFrequencyDict = obj_fetchDerivedFrequency.fetchDerivedFrequency(startDate,endDate)
    derivedVDIDict = obj_fetchDerivedVDI.fetchDerivedVDI(startDate)
    context = obj_dictMerger.dictMerger(derivedFrequencyDict['rows'], derivedFrequencyDict['weeklyFDI'],derivedVDIDict['VDIRows400Kv'],derivedVDIDict['VDIRows765Kv'])
    # print(context['rows400Kv'])

    definedTemplatePath = configDict['template_path'] + '\\freq_volt_1.docx'
    templateSavePath = configDict['template_path'] + '\\xyz.docx'
    doc = DocxTemplate(definedTemplatePath)
    doc.render(context)
    doc.save(templateSavePath)
    





