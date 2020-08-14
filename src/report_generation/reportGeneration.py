from src.repos.fetchDerivedFrequecny import FetchDerivedFrequency
from src.context_creator.dictMerger import DictMerger
import datetime as dt
from typing import List, Tuple
from docxtpl import DocxTemplate

def reportGeneration(startDate :dt.datetime, endDate:dt.datetime, configDict: dict)-> None:

    year = startDate.isocalendar()[0]
    week_number = startDate.isocalendar()[1]

    
    con_string= configDict['con_string_local']
    
    obj_fetchDerivedFrequency = FetchDerivedFrequency(con_string)
    obj_dictMerger = DictMerger(year, week_number, startDate, endDate)


    derivedFrequencyDict = obj_fetchDerivedFrequency.fetchDerivedFrequency(startDate,endDate)
    context = obj_dictMerger.dictMerger(derivedFrequencyDict['rows'], derivedFrequencyDict['weeklyVDI'])
    
    definedTemplatePath = configDict['template_path'] + '\\freq_volt_profile_raw_template.docx'
    templateSavePath = configDict['template_path'] + '\\frequencyOnly.docx'
    doc = DocxTemplate(definedTemplatePath)
    doc.render(context)
    doc.save(templateSavePath)
    





