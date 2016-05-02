#This file is calculate the time and distance using the Google Maps API

import csv
import googlemaps

#Method to convert time to the required format
def convert_time(time):
    print time
    minutes = 0
    tempdata = 0
    splittime = time.split(' ')
    for data in splittime:
        if data.isdigit():
            tempdata = int(data)
        else:
            if data == 'hours':
                minutes += (tempdata * 60)
            else:
                minutes += tempdata
    return minutes

#Method to check if the location exists
def location_exist(location):
    reader = csv.reader(open('E:\DBMS\Project\Test_Excel.csv', 'rb'), delimiter=',')
    for row in reader:
        if (row[0] == location[0] and row[1] == location[1]):
            return (row[2], row[3])

#Method to find the distance between a given source and destination
def find_distance(srcLat, srcLong, destLat, destLong):
    source = srcLat + ', ' + srcLong
    destination = destLat + ', ' + destLong
    location = [source, destination]
    retdata = location_exist(location)
    if retdata:
        return [retdata[0], retdata[1]]
    else:
        gmaps = googlemaps.Client(key='AIzaSyA_kZYf-DuWtfMcHFmxByAlyHFW0wjM3yw')
        distance = gmaps.distance_matrix(source, destination)
        drivedist = float(distance.get('rows')[0].get('elements')[0].get('distance').get('text').split(' ')[0].replace(',', ''))
        drivetime = convert_time(distance.get('rows')[0].get('elements')[0].get('duration').get('text'))
        print drivedist
        print drivetime
        writer = csv.writer(open('E:\DBMS\Project\Test_Excel.csv', 'a'), delimiter=',')
        result = [drivedist, drivetime]
        writer.writerow(result)
        return result

print find_distance("41.871027", "-87.662826", "40.769807", "-87.996358")