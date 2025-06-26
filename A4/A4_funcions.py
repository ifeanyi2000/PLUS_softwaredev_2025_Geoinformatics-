
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
from meteostat import Daily, Point, Normals, Monthly, Stations
import numpy
from geopy.distance import geodesic
from statsmodels.tsa.statespace.sarimax import SARIMAX

#get data from the nearest station to given coordinates that does not have NAs. plot the data of interest for a given time period
def dailyplot(coord,start,end,variables):
    start = datetime(start[0],start[1],start[2])
    end = datetime(end[0],end[1],end[2])
    print(start)
    print(end)


    stations = Stations()
    stations = stations.nearby(coord[0],coord[1])
    stationSbg2 = stations.fetch(100).dropna()
    # Get daily data for period
    data = Daily(stationSbg2.index[0], start, end)
    data = data.fetch()
    print(data)

    # Plot line chart including average, minimum and maximum temperature
    data.plot(y=variables)
    plt.show()
    return data

#get data from the n nearest stations to given coordinates from start to end. Also add the distance from the stations to the coordinates, which might be of use for the weather predictions (weather in areas more closely might have a higher influence than the weather far away)
def closest_stations(coord,n,start,end):
    stations = Stations()
    stations = stations.nearby(coord[0],coord[1])
    stationSbg2 = stations.fetch(n)
    indexes=stationSbg2.index
    data2=pd.DataFrame(columns=['tavg', 'tmin','tmax','prcp','snow','wdir','wspd','wpgt','pres','tsun','distance'])
    for i in indexes:
      data=Daily(str(i),start,end)
      data=data.fetch()
      stat=stationSbg2.loc[str(i)]
      locatio=(stat['latitude'],stat['longitude'])
      distance=geodesic(coord,locatio).km
      #print(distance)
      data=data.assign(distance=distance)
      #print(i)
      data2=pd.concat([data2,data])
    return data2

#compare normal temperature from period starting in year s1 with normal temperature from period starting in year s2. plot the changes. important for climate change analysis
def temperature_dev(coord,s1,s2):

    stations = Stations()
    stations = stations.nearby(coord[0],coord[1])
    stationSbg = stations.fetch(1000)
    stationSbg=stationSbg.dropna()

    data = Normals(stationSbg.index[0],s1,s1+29)
    data = data.fetch()

    data2 = Normals(stationSbg.index[0],s2,s2+29)
    data2 = data2.fetch()

    data3=data2-data
    data3.plot(y=['tavg', 'tmin', 'tmax'])
    plt.show()
    return data3
        
   
