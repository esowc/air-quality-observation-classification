# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 15:08:44 2020

@author: wegia
"""



import openaq

import pandas as pd

from pandas import json_normalize

import matplotlib.pyplot as plt

from datetime import datetime, date, time, timezone

import requests

import seaborn

import numpy as np

import json

import csv

df_DF = [];

MAX_RETRIES = 10

# Step 1 Initiatlise pyOpenAQ API
#
#  1 There are no edits 

print("  STEP 1 ")

print("********")

print("Initialise pyOpenAQ API")

api = openaq.OpenAQ()

ETCDIR = f"../etc"

print("OpenAQ pyOpenAPI begun")


def Milestone1_Get_Import_OpenAQ_Countries():

   status, resp = api.cities()

   #print(resp)

   resp_attribute = api.countries(df=True)

   df2 = resp_attribute.code

   df3 = pd.DataFrame(df2)

   print(resp_attribute)


   return df3


def Milestone1_Get_Measurements_OpenAQStations(StationOpenAQ, parameter): 

   OpenAQStations = []
   
   if(len(parameter) > 0):
     status, OpenAQmeasurementsrespno_pages = api.measurements(radius=1, date_to=dt_end, date_from=dt_begin, order_by="datetime", sort="asc",offset=0, page=1, limit=10000)
   
#    country='US', 
   # 'BE' 
   
     print(status) 
   
   if(len(parameter) == 0): 
  
     status, OpenAQmeasurementsrespno_pages = api.measurements(country_id='BE',date_to=dt_end, date_from=dt_begin,order_by="date", sort="asc", limit=10000)
   
 #  print(OpenAQmeasurementsrespno_pages)  
  
   OpenAQmeasurementsno_pages = int(OpenAQmeasurementsrespno_pages["meta"]["pages"]) 
 
   
   print(OpenAQmeasurementsno_pages)
   
   
   for page_num in range(1, OpenAQmeasurementsno_pages + 1):

      print(page_num)        

      res1 = Milestone1_Get_OpenAQ_Dataset_Measurement_OpenAQStation_perStation(StationOpenAQ, parameter, page_num) 
    
    #  print(res1)
      
      
    
      OpenAQStations.append(res1)
      
   return OpenAQStations 

def Milestone1_Get_OpenAQ_Dataset_Measurement_OpenAQStation_perStation(StationOpenAQ, parameter, page_num):
    
#Step 1 Choose the measurement country to import and parameter 
    
    res1 = None

    for ii in range(1, MAX_RETRIES + 1):

       try:
            if(len(parameter) == 1): 
                res1 = api.measurements(
                    country='BE', 
                  #  parameter=parameterselected, 
                    date_to=dt_end, 
                    date_from=dt_begin,
                    limit=10000, 
                    page=page_num,
                    df=True
                 )
               
            else: 
               
                print(parameter)
                
              
                res1 = api.measurements(
                    country='BE', 
                    # 'StationOpenAQ,  
                    date_to=dt_end, 
                    date_from=dt_begin,
                    order_by="datetime",
                    sort="asc",
                    limit=10000,
                    page=page_num,
                    df=True
                )
       
       except openaq.exceptions.ApiError:
            time.sleep(5)
            continue
       else:
            break
        
        
    print("Completed measurements ")

    return res1

def Milestone1_Get_Import_Count_OpenAQ_Station(OpenAQSelect):
 
   OpenAQStations = open(f"all_openaq_locations.json")
   OpenAQlocations = json.loads(OpenAQStations.read())
   OpenAQStationslength = len(OpenAQlocations)
   
   print(type(OpenAQlocations))
   
   OpenAQStationcount = 0
   
   SelectionOpenAQ = 0
   
   df = pd.DataFrame(OpenAQlocations)
   
   print(df[df['country']==OpenAQSelect].dtypes)
    
   print(df[df['country']==OpenAQSelect]['countsByMeasurement'])
   
    
   print(df[df['country']==OpenAQSelect]['count'])
   
   
   start_dt = datetime.strptime(OpenAQlocations[SelectionOpenAQ]["firstUpdated"], "%Y-%m-%dT%H:%M:%S.%fZ")
   end_dt = datetime.strptime(OpenAQlocations[SelectionOpenAQ]["lastUpdated"], "%Y-%m-%dT%H:%M:%S.%fZ")

   print(start_dt)

   print(end_dt)    

   return df[df['country']==OpenAQSelect]['location']



def Milestone1_Getparameter(Reqparameter):
    
    if(int(Reqparameter) < 10):
       
        Requestparameter = "-0" + Reqparameter

    else:

        Requestparameter = Reqparameter 
        
    return Requestparameter
    

def Milestone1_OpenAQ_API_Get_Measurements_APIoneStation(OpenAQSelects, OpenAQversion):

   Countryid= 'BE'

 
 #  print(dt_begin)
#
   
   Reqparameter = []
     
   OpenAQdf = []
   
   Reqparameter.append(Milestone1_Getparameter(str(dt_begin.month)))
     
   Reqparameter.append(Milestone1_Getparameter(str(dt_begin.day)))
     
   Reqparameter.append(Milestone1_Getparameter(str(dt_end.month)))
     
   Reqparameter.append(Milestone1_Getparameter(str(dt_end.day)))
     
   
   try:
    
     parametersort = "https://u50g7n0cbj.execute-api.us-east-1.amazonaws.com/v1/measurements?date_from=" + str(dt_begin) + "&date_to=" + str(dt_end) + "&limit=100&page=1&offset=0&country=AE&sort=desc&radius=1&order_by=datetime"  
    
#    "2000-01-01T00%3A00%3A00%2B00%3A00"
    
#    2021-02-05T12%3A00%3A00%2B00%3A00"

 #   response = requests.get("https://docs.openaq.org/v2/measurements?limit=100&page=1&offset=0&sort=desc&radius=1000")  
    
   #  print(parametersort)
     
   
     parameterrequest1 = "https://docs.openaq.org/v1/measurements?" 
   
     paramerterrequestv2 = "https://docs.openaq.org/v2/measurements?"
    
    
    
     parameterrequest = "https://u50g7n0cbj.execute-api.us-east-1.amazonaws.com/v1/measurements?date_from=" + str(dt_begin.year) + Reqparameter[0] +  Reqparameter[1]  + "T00%3A00%3A00%2B00%3A00&date_to=" + "2021" + Reqparameter[2]  + Reqparameter[3] + "T12%3A00%3A00%2B00%3A00&limit=10000&sort=desc&" + "country=" + OpenAQSelects['country'] + "&radius=1&order_by=datetime"
     
     # https://u50g7n0cbj.execute-api.us-east-1.amazonaws.com/
     
   #  response = requests.get("https://u50g7n0cbj.execute-api.us-east-1.amazonaws.com/v1/measurements?date_from=" + str(dt_begin.year) + Reqparameter[0] +  Reqparameter[1]  + "T00%3A00%3A00%2B00%3A00&date_to=" + "2021" + Reqparameter[2]  + Reqparameter[3] + "T12%3A00%3A00%2B00%3A00&limit=10000&sort=desc&" + "country=" + OpenAQSelects['country'] + "&radius=1&order_by=datetime")
  
  #   responseno = response["meta"]["pages"]
   
     print(OpenAQSelects['parameter'])
     
     if(len(OpenAQSelects['parameter']) > 0):
         
         parameterrequest += "&parameter=" + OpenAQSelects['parameter'][0] 
     
     response = requests.get(parameterrequest)
   
     responseno = response.json()["meta"]# ["found"]/10000
     
     responseno = int(responseno["found"]/OpenAQSelects["limit"])
     
     print("request")
     
     print(responseno)  
   
   #  print(response.json()) 
 
     
     if(response.status_code == 200):
            resp = response.json()["results"]
    
            OpenAQdfresp = pd.DataFrame(resp)
            print(OpenAQdfresp["date"])  
            OpenAQdfresp = Milestone2_Convert_DateFormat(OpenAQdfresp)

            OpenAQdfresp.index = OpenAQdfresp['date.utc']
       
     
     OpenAQdf.append(OpenAQdfresp)
        
     
     OpenAQreq = range(2, responseno)
   
     
     print(OpenAQreq)
     
     
     for page_num in range(2, responseno + 1):

        print(" append ") 
        print(str(page_num)) 
        OpenAQrequestparameterrequest = parameterrequest + "&page=" + str(page_num)           

        response = requests.get(OpenAQrequestparameterrequest)
     
     #  print(response.json())
      
        if(response.status_code == 200):
            resp = response.json()["results"]
    
            OpenAQdfresp = pd.DataFrame(resp)
            print(OpenAQdfresp["date"])  
            OpenAQdfresp = Milestone2_Convert_DateFormat(OpenAQdfresp)

            OpenAQdfresp.index = OpenAQdfresp['date.utc']
       
     
        OpenAQdf.append(OpenAQdfresp)
        
    # str(dt_begin.month)
    # + str(dt_begin.day)
    
#    + str(dt_end.month)
  #    + str(dt_end.day) 
    
   #  response = requests.get("https://u50g7n0cbj.execute-api.us-east-1.amazonaws.com/v1/measurements", params=parameters)
     
    # "https://api.openaq.org/v1/measurements"
  #   df = json.dump(response.json()["results"])
   #  json.dump(all_locations)

  #   print(df)

   #  df = json.loads(df)
     
   except:
   
      pass
  
   print(response.status_code)
   
   print(OpenAQdf)
   
   return OpenAQdf



def Milestone2_Convert_DateFormat(DatasetOpenAQ):
    
#How to split column into two columns
#https://www.geeksforgeeks.org/split-a-text-column-into-two-columns-in-pandas-dataframe/
 
  # print(DatasetOpenAQ.dtypes) 

   DatasetOpenAQ[['Dateutc','Datelocal']] = DatasetOpenAQ.date.apply(lambda x: pd.Series(str(x).split(",")))


   Dataset_split = DatasetOpenAQ.Dateutc.apply(lambda x: pd.Series(str(x).split("':")))


   DatasetOpenAQ['date.utc'] = pd.to_datetime(Dataset_split[1])

 #  print(DatasetOpenAQ)

  # print(DatasetOpenAQ['value'])

   pd.to_datetime(DatasetOpenAQ['date.utc'])

   return DatasetOpenAQ


def Milestone1_Get_Import_OpenAQ_Dataset_One_Statonselect(OpenAQSelects, iterationamount,  OpenAQrequest):

 
   if(OpenAQrequest == 0):    

       OpenAQversion = 1      

       Sortres = Milestone1_OpenAQ_API_Get_Measurements_APIoneStation(OpenAQSelects, OpenAQversion)

       print(Sortres)

   if(OpenAQrequest == 1):    
       
       OpenAQversion = 2
       
       Sortres = Milestone1_OpenAQ_API_Get_Measurements_APIoneStation(OpenAQSelects, OpenAQversion)
 
 
    
   if(OpenAQrequest == 2):    

       Sortres = [] 

       Sort = Milestone1_Get_Import_Count_OpenAQ_Station(OpenAQSelects['country']) 

       print(Sort)
   
       for SortAppend in Sort: 
   
           print(type(SortAppend))
     
           res = Milestone1_Get_Import_OpenAQ_Dataset_One_Station(SortAppend, OpenAQSelects['parameter'], iterationamount, OpenAQSelects)

           Sortres.append(res)
   
   if(OpenAQrequest == 3):    

       Sortres = [] 

       
       df4 = Milestone1_Get_Measurements_OpenAQStations(OpenAQSelects['country'], OpenAQSelects['parameter'])  
     
       Sortres.append(df4)
        
   if(OpenAQrequest > 3):
        
       print(Sortres)
   
   return Sortres   
           

def Milestone1_Get_Import_OpenAQ_Dataset_One_Station(OpenAQStation, parameter, iterationamount, OpenAQSelect):

   print(type(OpenAQStation))  

   Completedreq = 0
   
   res_1 = None
   
   # Step 1 Get Measurements for station
   try: 
    
     res_1 = api.measurements(location=OpenAQStation, parameter=parameter, date_to=dt_end, date_from=dt_begin, df=True, limit=10000)
     print(res_1)
  
   except:
     pass   
    
   

   return res_1

 #   https://u50g7n0cbj.execute-api.us-east-1.amazonaws.com/v1/measurements?date_from=2000-01-01T00%3A00%3A00%2B00%3A00&date_to=2021-02-08T12%3A15%3A00%2B00%3A00&limit=100&page=1&offset=0&sort=desc&radius=1000&location=US%20Diplomatic%20Post%3A%20Abu%20Dhabi&location=US%20Diplomatic%20Post%3A%20Dubai%2C%20Dubai&location=Abu%20Dhabi&order_by=datetime
    
def Milestone1_Get_Measurement_OpenAQStations(OpenAQ_Stations, Completed_QC_Processes, parameter):
     
    
   iteration1 = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','64','65','66','67','68','69','70','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97','98','99','100','101','102','103','104','105','106','107','108','109','110','111','112','113','114','115','116','117','118','119','120','121','122','123','124','125','126','127','128','129','130','131','132','133','134','135','136','137','138','139','140','141','142','143','144','145','146','147','148','149','150','151','152','153','154','155','156','157','158','159','160','161','162','163','164','165','166','167','168','169','170','171','172','173','174','175','176','177','178','179','180','181','182','183','184','185','186','187','188','189','190','191','192','193','194','195','196','197','198','199','200','201','202','203','204','205','206','207','208','209','210','211','212','213','214','215','216','217','218','219','220','221','222','223','224','225','226','227','228','229','230','231','232','233','234','235','236','237','238','239','240','241','242','243','244','245','246','247','248','249','250','251','252','253','254','255','256','257','258','259','260','261','262','263','264','265','266','267','268','269','270','271','272','273','274','275','276','277','278','279','280','281','282','283','284','285','286','287','288','289','290','291','292','293','294','295','296','297','298','299','300','301','302','303','304','305','306','307','308','309','310','311','312','313','314','315','316','317','318','319','320','321','322','323','324','325','326','327','328','329','330','331','332','333','334','335','336','337','338','339','340','341','342','343','344','345','346','347','348','349','350','351','352','353','354','355','356','357','358','359','360','361','362','363','364','365','366','367','368','369','370','371','372','373','374','375','376','377','378','379','380','381','382','383','384','385','386','387','388','389','390','391','392','393','394','395','396','397','398','399','400','401','402','403','404','405','406','407','408','409','410','411','412','413','414','415','416','417','418','419','420','421','422','423','424','425','426','427','428','429','430','431','432','433','434','435','436','437','438','439','440','441','442','443','444','445','446','447','448','449','450','451','452','453','454','455','456','457','458','459','460','461','462','463','464','465','466','467','468','469','470','471','472','473','474','475','476','477','478','479','480','481','482','483','484','485','486','487','488','489','490','491','492','493','494','495','496','497','498','499','500','501','502','503','504','505','506','507','508','509','510','511','512','513','514','515','516','517','518','519','520','521','522','523','524','525','526','527','528','529','530','531','532','533','534','535','536','537','538','539','540','541','542','543','544','545','546','547','548','549','550','551','552','553','554','555','556','557','558','559','560','561','562','563','564','565','566','567','568','569','570','571','572','573','574','575','576','577','578','579','580','581','582','583','584','585','586','587','588','589','590','591','592','593','594','595','596','597','598','599','600','601','602','603','604','605','606','607','608','609','610','611','612','613','614','615','616','617','618','619','620','621','622','623','624','625','626','627','628','629','630','631','632','633','634','635','636','637','638','639','640','641','642','643','644','645','646','647','648','649','650','651','652','653','654','655','656','657','658','659','660','661','662','663','664','665','666','667','668','669','670','671','672','673','674','675','676','677','678','679','680','681','682','683','684','685','686','687','688','689','690','691','692','693','694','695','696','697','698','699','700','701','702','703','704','705','706','707','708','709','710','711','712','713','714','715','716','717','718','719','720','721','722','723','724','725','726','727','728','729','730','731','732','733','734','735','736','737','738','739','740','741','742','743','744','745','746','747','748','749','750','751','752','753','754','755','756','757','758','759','760','761','762','763','764','765','766','767','768','769','770','771','772','773','774','775','776','777','778','779','780','781','782','783','784','785','786','787','788','789','790','791','792','793','794','795','796','797','798','799','800','801','802','803','804','805','806','807','808','809','810','811','812','813','814','815','816','817','818','819','820','821','822','823','824','825','826','827','828','829','830','831','832','833','834','835','836','837','838','839','840','841','842','843','844','845','846','847','848','849','850','851','852','853','854','855','856','857','858','859','860','861','862','863','864','865','866','867','868','869','870','871','872','873','874','875','876','877','878','879','880','881','882','883','884','885','886','887','888','889','890','891','892','893','894','895','896','897','898','899','900','901','902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924','925','926','927','928','929','930','931','932','933','934','935','936','937','938','939','940','941','942','943','944','945','946','947','948','949','950','951','952','953','954','955','956','957','958','959','960','961','962','963','964','965','966','967','968','969','970','971','972','973','974','975','976','977','978','979','980','981','982','983','984','985','986','987','988','989','990','991','992','993','994','995','996','997','998','999','1000']

   iterationamount = 0 
 
   DF_OpenAQDataset = []
    
   for OpenAQStation in OpenAQ_Stations:

      print(OpenAQStation) 
      
      if(iterationamount >= Completed_QC_Processes):
      
        if(iterationamount == 0):
          OpenAQStation_Dataset = Milestone1_Get_Import_OpenAQ_Dataset_One_Staton(OpenAQStation, parameter, iteration1[iterationamount])
          DF_OpenAQDataset.append(OpenAQStation_Dataset)
          
          print(OpenAQStation_Dataset)
    
        else:
          
          OpenAQStation_ImportDataset = Milestone1_Get_Import_OpenAQ_Dataset_One_Staton(OpenAQStation, parameter, iteration1[iterationamount])
          DF_OpenAQDataset.append(OpenAQStation_ImportDataset)
       #   OpenAQStation_Dataset.append(OpenAQStation_ImportDataset, ignore_index=True) 
          print(OpenAQStation_ImportDataset)
          
      iterationamount = iterationamount + 1
     
    
   return DF_OpenAQDataset
    

def Milestone1_Get_Import_OpenAQ_EveryStation_inChoosenCountry(OpenAQ_StationCountry):

    
   result1 = api.cities(country=OpenAQ_StationCountry, df=True, limit=10000)
    
   print(result1)
    
   for index, res1 in result1.iterrows():
       
      if(res1['name'] != "N/A"):
          
       result = api.locations(city=res1['city'], df=True)

       for index1, res2 in result.iterrows():
             
           df_DF.append(res2['location'])
       
     

   
   
   return df_DF  

def Milestone1_Get_Parameters(OpenAQSelect, parameterselected, dt_begin, dt_end):
   
   OpenAQSelects = {
      "radius": 1,
      "country":OpenAQSelect,
    #  "location": station1,
      "parameter": parameterselected,
      "date_from": dt_begin,
      "date_to": dt_end,
      "limit": 10000
   }

   print(OpenAQSelects['radius'])

   return OpenAQSelects
    
def Milestone1_Get_Measurements_CSV_OpenAQStation(OpenAQ_Stations, SelectionOpenAQChoose, parameter, SelectionOpenAQ, dt_begin, dt_end, SelectionDatasetOpenAQ):
    
   OpenAQDataset = r'OpenAQ_Dataset'
 
   SelectedOpenAQ = "Selection"
   
   if(SelectionOpenAQ == 0):
     SelectedOpenAQ = "One Station"
      
   if(SelectionOpenAQ == 1):
     SelectedOpenAQ = "CoordinateCentreandRadius"
  
   if(SelectionOpenAQ == 2):
     SelectedOpenAQ = "Country"
   
    
   OpenAQDataset = OpenAQDataset + " " + SelectionOpenAQChoose + " " + parameter + " " + SelectedOpenAQ + " " +  str(dt_begin) + " to " + str(dt_end) + ".csv" 
    
   print("Printed OpenAQ import to ")
   
   print( OpenAQDataset)

   if(SelectionDatasetOpenAQ == 0):   
    OpenAQ_Stations.to_csv(OpenAQDataset, mode='w', index=False)                       
 
   if(SelectionDatasetOpenAQ == 1):
    OpenAQ_Stations.to_csv(OpenAQDataset, header=False, index=False, mode='a+') 

#Step 1 Choose the measurement country to import and Time Schedule
#
# 1 Choose from output of Country Codes 
#
# SelectionchooseOpenAQ
#
# 2 Change country code in CountryCode
#
# dt_begin = date(2020,3,1)  # Edit
# dt_end = date(2020,9,1)  # Edit

# res1 = api.measurements(country='IN', parameter='pm25', date_to=dt_end, date_from=dt_begin, limit=10000, df=True)
#
# 3 Test un comment   
#

#  SelectionchooseOpenAQ = 'AG'

# reports measurements for station
# 
# result = Test_Milestone3_Import_OpenAQ_Dataset_Station()
#
# Test_Milestone3_Import_OpenAQ_Dataset_StationOpenAQ('Altınova-MTHM')

# print("Choose from ")

# OpenAQ_Countries = Milestone1_Get_Import_OpenAQ_Countries()

#OpenAQStations = Milestone1_Get_Import_OpenAQ_EveryStation_inChoosenCountry(CountryCode)


SelectionchooseOpenAQ = 'BE' # 'AE'  # Edit

dt_begin = date(2020,3,1)  # Edit
dt_end = date(2020,3,4)  # Edit

print("Getting OpenAQ dataset from OpenAQ API from ") 
print(dt_begin)
print(" to ")
print(dt_end)
print(" for every OpenAQ Station and parameter ")


# Step 2 Choose parameter 
#
#
# 1 Choose to import one parameter or all parameters for OpenAQ Station
#
#  Change parameter to pm25, pm10, no2, bc, so2, o3
#
#  Change to 1 All OpenAQ parameters or 0 - One parameter and select it
#
# Change parameter = '' to selected
#

print("  STEP 2 ")

print("********")

SelectEveryParameter_YesorNo = 0 # Edit 1 Yes 0 No just one 

parameterselected = 'pm25'  # Edit

parameter_selection = []

print("Parameter chosen")

if(SelectEveryParameter_YesorNo == 0):
    
   parameter_selection.append(parameterselected)

   print(parameter_selection)

if(SelectEveryParameter_YesorNo == 1):
    
   print("Every parameter at selected or chosen OpenAQ station") 

# Step 3
#
# 1 Choose Source
#
#
#  0 - The OpenAQ API version 1 from source or
#  1 OpenAQ API version 2 from source or 2 - The py-OpenAQ API using select every Location 3 - The py-OpenAQ using select Country
#
#
#
#
#  
#
#  OpenAQrequest = 0 

print("  STEP 3 ")

print("********")


OpenAQrequest = 0 # Edit 0 - The OpenAQ API version 1 from source or 1 OpenAQ API version 2 from source or 2 - The py-OpenAQ API using select every Location 3 - The py-OpenAQ using select Country

print("Source of OpenAQ requests")

if(OpenAQrequest == 0): print("0 - The OpenAQ API version 1 from source")
if(OpenAQrequest == 1): print("1 OpenAQ API version 2 from source" )
if(OpenAQrequest == 2): print("2 - The py-OpenAQ API using select every Location") 
if(OpenAQrequest == 3): print("3 - The py-OpenAQ using select Country")

iterationamount = 0

OpenAQSelects = Milestone1_Get_Parameters(SelectionchooseOpenAQ, parameter_selection, dt_begin, dt_end)

OpenAQselection = Milestone1_Get_Import_OpenAQ_Dataset_One_Statonselect(OpenAQSelects, iterationamount, OpenAQrequest)

Completed_QC_Processes = 0

# OpenAQDataset = Milestone1_Get_OpenAQ_Dataset_Measurement_OpenAQStation_perStation(CountryCode, parameter_selection, 1)

# OpenAQDatasetselection = Milestone1_Get_Measurements_OpenAQStations(StationOpenAQ, parameter_selection)

print(OpenAQselection)

# Milestone1_Get_Import_Count_OpenAQ_Station()

# Milestone1_Get_Import_OpenAQ_Dataset_One_Staton(OpenAQStation, parameterselected, iterationamount)


print("  STEP 4 ")

print("********")

print("Results")

if(len(OpenAQselection) == 0):
  
  print("*****") 
  
  print("API Error")
    
  print("The API returned an error because") 
 
  if(OpenAQrequest < 2): 
      
     print("the request was inaccurate")
      
     print("The API parameters may have been edited please check OpenAQ.org API page")
        
  if(OpenAQrequest > 1):
        
     print("it was unavailable after trying this many requests ")  
  
     print(MAX_RETRIES)
  
     print("Try to the process again after a few minutes")


if(len(OpenAQselection) > 0):
 
   print("Found these Stations in selection")


   for OpenAQ_Station in OpenAQselection:
    
      OpenAQStations = OpenAQ_Station['location'].unique()

      print(OpenAQStations)
      
print("  STEP 5 ")

print("********")

print("print results to CSV")

SelectionOpenAQChoose = "unique debug" + SelectionchooseOpenAQ

SelectionOpenAQ = 2

SelectionDatasetOpenAQ = 0 

Milestone1_Get_Measurements_CSV_OpenAQStation(OpenAQselection[0], SelectionOpenAQChoose, parameterselected, SelectionOpenAQ, dt_begin, dt_end, SelectionDatasetOpenAQ)

SelectionDatasetOpenAQ = 1

iterationamount = 1

for OpenAQ_Station in OpenAQselection:

    
   if(len(OpenAQselection) > iterationamount):
     
     Milestone1_Get_Measurements_CSV_OpenAQStation(OpenAQselection[iterationamount], SelectionOpenAQChoose, parameterselected, SelectionOpenAQ, dt_begin, dt_end, SelectionDatasetOpenAQ)

     iterationamount = iterationamount + 1 
