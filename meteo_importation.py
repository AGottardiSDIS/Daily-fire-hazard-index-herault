import requests
import os
from datetime import date, timedelta
import config

token = config.token_meteo

def save_temperature(date, date_dem):
    #sous forme 2022-07-21 en str
    url_temp_arome = f"https://public-api.meteofrance.fr/public/arome/1.0/wcs/MF-NWP-HIGHRES-AROME-001-FRANCE-WCS/GetCoverage?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&format=image/tiff&coverageId=TEMPERATURE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND___{date}T12:00:00Z&subset=time({date_dem}T15:00:00Z)&subset=lat(43.156082016415894,44.392043930478394)&subset=long(2.3804016113281254,4.363433837890625)&subset=height(2)"
    r_aro = requests.get(url_temp_arome, {"apikey" : token})
    if(r_aro.status_code == 200):
        print("Download Temperature")

    with open(f'./Input/weather/{date_dem}/temp_{date_dem}_AROME.grib2', 'wb') as f:
        f.write(r_aro.content)

def save_vent(date, date_dem):
    #sous forme 2022-07-21 en str
    url_temp_arome = f"https://public-api.meteofrance.fr/public/arome/1.0/wcs/MF-NWP-HIGHRES-AROME-001-FRANCE-WCS/GetCoverage?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&format=image/tiff&coverageId=WIND_SPEED_GUST__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND___{date}T12:00:00Z&subset=time({date_dem}T15:00:00Z)&subset=lat(43.156082016415894,44.392043930478394)&subset=long(2.3804016113281254,4.363433837890625)&subset=height(10)"
    r_aro = requests.get(url_temp_arome, {"apikey" : token})
    if(r_aro.status_code == 200):
        print("Download Vent")

    with open(f'./Input/weather/{date_dem}/vent_{date_dem}_AROME.grib2', 'wb') as f:
        f.write(r_aro.content)


def save_HR(date, date_dem):
    #sous forme 2022-07-21 en str
    url_temp_arome = f"https://public-api.meteofrance.fr/public/arome/1.0/wcs/MF-NWP-HIGHRES-AROME-001-FRANCE-WCS/GetCoverage?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&format=image/tiff&coverageId=RELATIVE_HUMIDITY__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND___{date}T12:00:00Z&subset=time({date_dem}T15:00:00Z)&subset=lat(43.156082016415894,44.392043930478394)&subset=long(2.3804016113281254,4.363433837890625)&subset=height(2)"
    r_aro = requests.get(url_temp_arome, {"apikey" : token})
    if(r_aro.status_code == 200):
        print("Download Humidite Relative")

    with open(f'./Input/weather/{date_dem}/humidite_relative_{date_dem}_AROME.grib2', 'wb') as f:
        f.write(r_aro.content)

def save_precipitation(date, date_dem):
    #sous forme 2022-07-21 en str
    url_temp_arome = f"https://public-api.meteofrance.fr/public/arome/1.0/wcs/MF-NWP-HIGHRES-AROME-001-FRANCE-WCS/GetCoverage?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&coverageId=TOTAL_WATER_PRECIPITATION__GROUND_OR_WATER_SURFACE___2022-07-29T09:00:00Z&subset=time(2022-07-29T13:00:00Z)"
    r_aro = requests.get(url_temp_arome, {"apikey" : token})
    if(r_aro.status_code == 200):
        print("Download Precipitation")

    with open(f'./Input/weather/{date_dem}/precipitation_{date_dem}_AROME.grib2', 'wb') as f:
        f.write(r_aro.content)


def all_info(date_in):
    #date sous la forme 2022-07-21 en str du jour de calcul
    info = date_in.split("-") 
    day = date(int(info[0]), int(info[1]), int(info[2]))
    day_a = day + timedelta(days = 1)
    print(day, " ", day_a)
    
    # Check whether the specified path exists or not
    isExist = os.path.exists(f"./Input/weather/{day_a}/")

    if not isExist:
      
      # Create a new directory because it does not exist 
      os.makedirs(f"./Input/weather/{day_a}/")


    save_temperature(day, day_a)
    save_vent(day, day_a)
    save_HR(day, day_a)
    #save_precipitation(day, day_a) 

