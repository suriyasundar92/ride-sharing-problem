#This file interacts with the GraphHopper Directions API to get the distance and time between two points on the map

import json
from urllib2 import URLError, Request, urlopen

#Method to convert meters to miles
def meters_to_miles(distance):
    miles = distance / 1609.344
    return round(miles, 2)

#Method to convert milliseconds to minutes
def convert_time(time):
    minute, reminder = divmod(time, 60000)
    if reminder >= 50:
        minute += 1
    return minute

#Method to calculate distance and time for a given lat, long co-ordinates of source and destination
#Output will be in the following format [distance (miles), time (minutes)]
def find_distance(srcLat, srcLong, destLat, destLong):
    source = str(srcLat) + ',' + str(srcLong)
    destination = str(destLat) + ',' + str(destLong)
    requestString = "http://localhost:8989/route?point=" + source + "&point=" + destination
    #print requestString
    request = Request(requestString)

    try:
        response = urlopen(request)
        output = json.loads(response.read())
        paths = output["paths"]
        distance = meters_to_miles(paths[0]["distance"])
        time = convert_time(paths[0]["time"])
        result = [distance, time]
    except URLError:
        result = [-1, -1]

    return result

#Similar to the find distance method but takes two destinations instead of one
def find_distance_two(srcLat, srcLong, destLat, destLong, destLat1, destLong1):
    source = str(srcLat) + ',' + str(srcLong)
    destination = str(destLat) + ',' + str(destLong)
    destination1 = str(destLat1) + ',' + str(destLong1)
    requestString = "http://localhost:8989/route?point=" + source + "&point=" + destination + "&point=" + destination1
    print requestString
    request = Request(requestString)

    try:
        response = urlopen(request)
        output = json.loads(response.read())
        paths = output["paths"]
        distance = meters_to_miles(paths[0]["distance"])
        time = convert_time(paths[0]["time"])
        result = [distance, time]
    except URLError:
        result = [-1, -1]

    return result

#print find_distance(40.737015, -73.98833, 40.774783, -74.02082)
#print find_distance_two(40.737015, -73.98833, 40.774783, -74.02082, 40.744759, -74.060325)
#print find_distance_two(40.737015, -73.98833, 40.744759, -74.060325, 0, 0)