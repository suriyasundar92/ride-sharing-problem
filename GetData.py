#This file is to fetch trip details from the database

import MySQLdb
import data_model

#windowSize is the time window for which the data has to be pulled from the db
#dataLimit is the number of rows needed from the returned data set
#Output is a list of Trip objects
def GetData (windowSize, dataLimit):
    db = MySQLdb.Connect(host="localhost", port=3366, user="dbms", passwd="dbms", db="ridesharing")
    #sql = "select * from trip_details where pickup_time between '00:30:00' and '00:%s:00'" %str(30+windowSize)
    sql = "select * from trip_details where pickup_time <= '00:%s:00'" %windowSize

    if(dataLimit >= 1):
        sql = sql + "LIMIT %s" %dataLimit

    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    tripList = []
    for row in result:
        pLocation = data_model.Location(row[7], row[8])
        dLocation = data_model.Location(row[10], row[9])
        trip = data_model.Trip(int(row[0]), pLocation, dLocation, row[3], row[4], row[11], row[12])
        tripList.append(trip)

    cursor.close()
    db.close()
    return tripList

#trip_id - ID of the trip for which the details are required
#Output - A Trip object containing all the trip details
def GetTripDetails (trip_id):
    db = db = MySQLdb.Connect(host="localhost", port=3366, user="dbms", passwd="dbms", db="ridesharing")
    sql = "select * from trip_details where id = %s" %trip_id

    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    pLocation = data_model.Location(result[0][7], result[0][8])
    dLocation = data_model.Location(result[0][10], result[0][9])
    trip = data_model.Trip(int(result[0][0]), pLocation, dLocation, result[0][3], result[0][4], result[0][11], result[0][12])

    cursor.close()
    db.close()
    return trip
