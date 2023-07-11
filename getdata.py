import requests
import psycopg2 
import json
import datetime
#import mysql.connector

accessToken = ""

forcastUrl = "http://api.weatherapi.com/v1/forecast.json"

currentUrl = "http://api.weatherapi.com/v1/history.json"


#http://api.weatherapi.com/v1/history.json?key=0473901677084da5a4d234400222509&q=London&dt=2023-07-08

conn = psycopg2.connect(
    database="Weather_Data",
    user='postgres',
    password='password1',
    host='192.168.1.60',
    port='5432'
)


def call_api(url):

    r = requests.get(url)
    return r.json()

def saver_to_json(dic,filename):
    json_obj = json.dumps(dic)
    with open("/mnt/c/Users/EdThreadRipper/Documents/CodeProjects/WeatherProject/output/%s" % (filename), "w") as outfile:
        outfile.write(json_obj)
    return
def back_in_time(date):
    #Pretty sure this is not the best way to do this but it works
    splitDate = date.split("-")
    year = splitDate[0]
    month = splitDate[1]
    day = splitDate[2]
    dayInt = int(day)
    dayInt = dayInt - 1
    day = str(dayInt)
    if dayInt < 10:
        day = "0" + day
    newDate = year + "-" + month + "-" + day
    return newDate

def save_forcast_to_db(date, forcast_data, table_name):
    conn = psycopg2.connect(
    database="Weather_Data",
    user='postgres',
    password='password1',
    host='192.168.1.60',
    port='5432'
    )
    formated_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    print(type(formated_date))

    #print("INSERT into public.\"Forcast\"(\"Date\", maxtemp_c, maxtemp_f, mintemp_c, mintemp_f, totalprecip_mm, totalprecip_in, totalsnow_cm, avghumidity, daily_chance_of_rain, daily_chance_of_snow) VALUES (%s,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i)" % (formated_date,forcast_data['maxtemp_c'],forcast_data['maxtemp_f'],forcast_data['mintemp_c'],forcast_data['mintemp_f'],forcast_data['totalprecip_mm'],forcast_data['totalprecip_in'],forcast_data['totalsnow_cm'],forcast_data['avghumidity'],forcast_data['daily_chance_of_rain'],forcast_data['daily_chance_of_snow']))

    cursor = conn.cursor()
    cursor.execute("INSERT into public.\"Forcast\"(\"Date\", maxtemp_c, maxtemp_f, mintemp_c, mintemp_f, totalprecip_mm, totalprecip_in, totalsnow_cm, avghumidity, daily_chance_of_rain, daily_chance_of_snow) VALUES ('%s'::date,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i)"
                    % (formated_date,forcast_data['maxtemp_c'],forcast_data['maxtemp_f'],forcast_data['mintemp_c'],forcast_data['mintemp_f'],forcast_data['totalprecip_mm'],forcast_data['totalprecip_in'],forcast_data['totalsnow_cm'],forcast_data['avghumidity'],forcast_data['daily_chance_of_rain'],forcast_data['daily_chance_of_snow']))
    conn.commit()
    cursor.close()
    
    return

def get_forcast():
    

    forcast = call_api(forcastUrl + "?key=" + accessToken + "&q=14423&days=4&aqi=no&alerts=no")
    date = forcast['forecast']['forecastday'][0]['date']

    forcast_data = forcast['forecast']['forecastday'][0]["day"]
    save_forcast_to_db(date, forcast_data, "Forcast")
    
    historicDate = back_in_time(date)
    historic = call_api("%s?key=%s&q=14423&aqi=no&dt=%s" % (currentUrl,accessToken,historicDate))
    historic_data = historic['forecast']['forecastday'][0]["day"]
    #save_forcast_to_db(historicDate, historic_data, "Forcast")
    return


get_forcast()


