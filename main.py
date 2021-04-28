import requests as re
import pandas as pd
from pandas import json_normalize
import json
import csv
import time
import datetime
from datetime import date


d = datetime.date.today()
print(d)
unixtime = time.mktime(d.timetuple())
#print(unixtime)
fic_temp = "temp_ext.csv"

def get_api():
    #api2 = ("http://api.openweathermap.org/data/2.5/onecall/timemachine?lat=45.187604404569896&lon=5.704903862324499&units=metric&lang=fr&dt=1618992000&APPID=053c09565de3a966efa5b8d39b2969d9")

    api2 = "http://api.openweathermap.org/data/2.5/onecall/timemachine?"
    params = {
       'lat': '45.187604404569896',
       'lon': '5.704903862324499',
       'type': 'hour',
       'units': 'metric',
       'dt':  '1619308800',
       'lang': 'fr',
       'appid': '053c09565de3a966efa5b8d39b2969d9'
    }
    response = re.request("GET", api2, params=params)
    #print(response.url)
    #print(response.text)
    return response

def verif():
    try:
        if 'd' in open(fic_temp).read():
            print("Attention la date", d, "existe")
        else:
            print("Ne contient pas la date", d)
    except FileNotFoundError:
         print("le fichier", fic_temp, "n'existe pas")
         print("création du fichier", fic_temp, "...")
         pass

def conversion(test):
    
    data_dict = test.json()
    with open("data_file_1.json", "a") as write_file:
        json.dump(data_dict, write_file)

    df1 = json_normalize(data_dict['hourly'])
    #df1 = pd.io.json.normalize(data_dict['hourly'])
    #df1.to_csv("temp_ext_1.csv", mode='a', header=False)
    df1.dt = pd.to_datetime(df1['dt'],unit='s')
    selected_columns = df1[["dt","temp"]]
    df2 = selected_columns.copy()
    df2 = df2.set_index('dt')

    df3 = df2.resample('30min').interpolate().round(2)  # rééchantillonnage et interpolation 

    with open(fic_temp, "a") as f:
        df3.to_csv(f, header=f.tell()==0, index = True) #La méthode tell() de l’objet fichier retourne la position actuelle du curseur. Par conséquent, si le fichier est vide ou n’existe pas, f.tell==0 est True, de sorte que header est mis à True ; sinon, header est mis à False.

#verif()
var = get_api()
conversion(var)