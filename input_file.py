import data_model
from datetime import datetime
import csv
import logging
logging.basicConfig(filename="batching.log")

def get_trip_from_record(record_dict):
	pickup_location = data_model.Location(float(record_dict[" pickup_latitude"]), float(record_dict[" pickup_longitude"]))
	dropoff_location = data_model.Location(float(record_dict[" dropoff_latitude"]), float(record_dict[" dropoff_longitude"]))
	pickup_time = datetime.strptime(record_dict[" pickup_datetime"], "%Y-%m-%d %X")
	dropoff_time = datetime.strptime(record_dict[" dropoff_datetime"], "%Y-%m-%d %X")
	return data_model.Trip(record_dict["medallion"], pickup_location, dropoff_location, pickup_time, dropoff_time)


def get_batch(index):
	file_for_batch = 'trip_batch_' + str(index+1) + '.csv'
	csv_reader = csv.DictReader(open(file_for_batch,'r'))
	first_record = next(csv_reader)
	print(first_record)
	trip_for_first_record = get_trip_from_record(first_record)
	batch_list = [get_trip_from_record(first_record)]
	try:
		record = next(csv_reader)
		trip_for_record = get_trip_from_record(record)
		while True:
			batch_list.append(trip_for_record)
			record = next(csv_reader)
			trip_for_record = get_trip_from_record(record)
	except StopIteration:
		pass
	return batch_list

def batch_input_file(input_file):
	csv_reader = csv.DictReader(input_file)
	first_record = next(csv_reader)
	trip_for_first_record = get_trip_from_record(first_record)
	try:
		batch_index = 0
		while True:
			batch_index += 1
			batch_file = open('trip_batch_' + str(batch_index) + '.csv', 'w')
			batch_csv_writer = csv.DictWriter(batch_file, csv_reader.fieldnames)
			batch_csv_writer.writeheader()
			record = next(csv_reader)
			trip_for_record = get_trip_from_record(record)
			while (trip_for_record.pickup_time - trip_for_first_record.pickup_time).total_seconds() < 60*data_model.WINDOW_SIZE_IN_MIN:
				try:
					record = next(csv_reader)
					trip_for_record = get_trip_from_record(record)
					batch_csv_writer.writerow(record)
				except Exception:
					logging.error(str(record))
			first_record = record
			trip_for_first_record = trip_for_record
	except StopIteration:
		pass

#def get_trips_for_batch():


if __name__ == "__main__":
	data_file = open("trip_data_1.csv")
	batch_input_file(data_file)
