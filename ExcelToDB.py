#This file is to load data from the given excels into the database
#Before loading the data, this checks for the source's proximity to the JFK airport

import MySQLdb
import csv
import datetime
import HopperDistance

#Database connection
db = MySQLdb.Connect(host="localhost", port=3366, user="dbms", passwd="dbms", db="ridesharing")
cursor = db.cursor()
db.autocommit(True)

#Opening the CSV file
csv_data = csv.reader(open("E:\\DBMS\\Project\\trip_data_1.csv"))

#Looping through all the data in CSV and inserting them into the database
dataCount = 0
for data in csv_data:
    if dataCount > 0:
        if float(data[12]) != 0 and float(data[13]) != 0:
            result = HopperDistance.find_distance(data[13], data[12], 40.644104, -73.782665)
            if result[0] >= 3:
                #result = HopperDistance.find_distance(data[13], data[12], 40.644104, -73.782665)
                pickup_time = datetime.datetime.strptime(data[5], "%Y-%m-%d %H:%M:%S")
                drop_time = datetime.datetime.strptime(data[6], "%Y-%m-%d %H:%M:%S")
                sql = "insert into trip_details (trip_id, trip_date, pickup_time, dropoff_time, trip_time, trip_distance, pickup_lat, pickup_long, dropoff_lat, dropoff_long, distance, travel_time) values (%s, '%s', '%s', '%s', %s, %s, '40.644104', '-73.782665', '%s', '%s', %s, %s)" % (int(data[0]), pickup_time.date().strftime("%Y-%m-%d"), pickup_time.time().strftime("%H:%M:%S"), drop_time.time().strftime("%H:%M:%S"), int(data[8]), float(data[9]), float(data[12]), float(data[13]), result[0], result[1])
                #print sql
                cursor.execute(sql)
                #db.commit()
    #print data
    rowFlag = True
    dataCount += 1

print 'Rows inserted: %s' %dataCount
cursor.close()
db.close()