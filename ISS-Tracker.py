#https://janakiev.com/blog/gps-points-distance-python/
#http://open-notify.org/Open-Notify-API/ISS-Pass-Times/
# Youtube Reference https://www.youtube.com/watch?v=lal6eWVCEJs
# Youtube Reference https://www.youtube.com/watch?v=IVBD_V42tXI&t=534s
#http://api.open-notify.org/
#https://www.ridgesolutions.ie/index.php/2013/11/14/algorithm-to-calculate-speed-from-two-gps-latitude-and-longitude-points-and-time-difference/


# FINAL CODE FOR International Space Station(ISS) tracker
import requests
import pandas as pd
from IPython.display import Image
from geopy.geocoders import Nominatim
from  pytz import utc
from datetime import datetime
import os
os.environ["PROJ_LIB"] = "C:\\Continuum\\anaconda3\\Library\\share"
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import time
import pyproj
import warnings
warnings.filterwarnings("ignore")


print('WELCOME TO THE INTERNATIONAL SPACE STATION (ISS) TRACKER, SELECT 1 OR 2')
answer= int((input('1: NEXT ISS PASS BY IN YOUR SELECTED LOCATION  2: WHERE IS ISS NOW  :    ' )))

# CASE 1 - FIND ISS LOCATION

if answer == 1:
    enter_location =input('PLEASE ENTER YOUR LOCATION ? ' )     
    geolocator = Nominatim(user_agent="iss")
    location = geolocator.geocode(enter_location)
    
    #print(location.address)
    #print((location.latitude, location.longitude))
    
    lat = location.latitude
    lon = location.longitude
    
    url_iss_pass = 'http://api.open-notify.org/iss-pass.json'
    location={'lat':lat,'lon':lon}
    response= requests.get(url_iss_pass,params=location).json()
    
    if response['message']=='success':
        for i in range(len(response)):
            
            next_pass_ts= response['response'][i]['risetime']
            duration= response['response'][i]['duration']
            next_pass=datetime.fromtimestamp(next_pass_ts , tz=utc)

            # SECONDS TO MINUTE CONVERSION.
            day = duration // (24 * 3600)
            time = day % (24 * 3600)
            hour = time // 3600
            time %= 3600
            minutes = duration // 60
            time %= 60
            seconds = time

            print('-----INTERNATIONAL SPACE STATION TRACKER-----')
            print('Location\t\t\t{}'.format(enter_location))
            print('UTC Date & Time\t\t\t{} '.format(next_pass))
            print('Flyby Duration in minutes\t{}:{}' .format(minutes,seconds))

        #print('The ISS will fly by {} on {} for {} minutes and {} seconds  '.format(enter_location,next_pass,minutes,seconds))
            
# CASE 2 - TRACK THE CURRENT ISS LOCATION 
    
elif answer == 2:
        
        def get_space_space_station_location():
            r=requests.get(url="http://api.open-notify.org/iss-now.json")
            space_station_location=(r.json())
            space_station_longitudes=float(space_station_location['iss_position']['longitude'])
            print('ISS Long',space_station_longitudes)
            space_station_latitudes=float(space_station_location['iss_position']['latitude'])
            print('ISS Lat',space_station_latitudes)
            return(space_station_longitudes,space_station_latitudes)
       

        
        my_dpi=96
        plt.figure(figsize=(16,8))
        m=Basemap(llcrnrlon = -180 , llcrnrlat=-65, urcrnrlon = 180,urcrnrlat = 80)
        m.drawmapboundary(fill_color='#A6CAE0',linewidth=0)
        m.fillcontinents(color='grey',alpha=0.3)
        m.drawcoastlines(linewidth=0.1,color='white')
        space_staton_longitude,space_staton_latitude=get_space_space_station_location()
        m.scatter(space_staton_longitude,space_staton_latitude,s=200,alpha =0.4 , color ='red')
        #plt.title('Current International Space Station Position', fontsize=30)
        
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent="iss")
        location = geolocator.reverse("{},{}".format(space_staton_latitude,space_staton_longitude))
        
        
        if location.address == None :
            print("Can't determine current passing location")
        else:
            print("Current Passing Location is "+location.address)

# TRACK ISS SPEED.
        geod = pyproj.Geod(ellps='WGS84')

        def get_space_space_station_location():
            r=requests.get(url="http://api.open-notify.org/iss-now.json")
            space_station_location=(r.json())
            space_station_longitudes=float(space_station_location['iss_position']['longitude'])
            space_station_latitudes=float(space_station_location['iss_position']['latitude'])
            return(space_station_longitudes,space_station_latitudes)

        lon0, lat0 = get_space_space_station_location()
        z=3
        time.sleep(z)
        lon1, lat1 = get_space_space_station_location()
        azimuth1, azimuth2, dist = geod.inv(lon0, lat0, lon1, lat1)
        speed_mps=(dist/3)
        speed_kph=(speed_mps*3600.0)/1000.0     
        #print("ISS is travelling at " + str(round(speed_kph)) +" Kilometer / Hour")
        plt.title('INTERNATONAL SPACE STATION POSITION\n'+'SPEED ' +str(round(speed_kph)) +" kilometer/hour", fontsize=15)
        
        #speed_mps=(dist/3)
        #speed_kps=(speed_mps)/1000
        #speed_kph=(speed_mps*3600)/1000     
        #print("ISS is travelling at " + str(round(speed_kps)) +" Kilometer / Second")
        #plt.title('INTERNATONAL SPACE STATION POSITION\n'+'Speed ' +str(round(speed_kps)) +" Kilometer/Second", fontsize=15)
        
               
else:
        print('Wrong Answer') 
        
        
