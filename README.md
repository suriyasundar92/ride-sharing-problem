# ride-sharing-problem

This problem deals with sharing of trips among a large pool of data set taken from a public data collection

Below are the steps to run the source code in any local machine,

Download the source code from the GitHub by following the link https://github.com/suriyasundar92/ride-sharing-problem.git

Setup GraphHopper Server.

	Download the required files by following the link https://github.com/graphhopper/graphhopper/blob/0.6/docs/web/quickstart.md

	We will have to download the OSM data of the area under which we would like to run the algorithm. The OSM data can be downloaded from the OSM website http://wiki.openstreetmap.org/wiki/Downloading_data.

	GraphHopper routing service can be setup by running the jar file for the service by execute the following command in command prompt,

	java -jar *.jar jetty.resourcebase=webapp config=config-example.properties osmreader.osm=new-york_new-york.osm.pbf

Download and Install the NetworkX library for Python

Setup the MySQL Database in the local machine

Create a table in the MySQL Database by executing the following query,                           
create table trip_details (id int not null auto_increment primary key, trip_id int not null, trip_date date, pickup_time time, dropoff_time time, trip_time int, trip_distance float, pickup_lat varchar(15), pickup_long varchar(15), dropoff_lat varchar(15), dropoff_long varchar(15), distance float, travel_time int)

Execute the Python file ExcelToDB.py to load all data from excel to the newly created table in the MySQL database.

Once the database is populated with the required data, set the parameters Walking Threshold, Merging Threshold and Window Size in the python file named trip_merging.py, after setting the parameters run the file in Python

The merged and lone trips will be printed soon after merging algorithm finishes its process.
