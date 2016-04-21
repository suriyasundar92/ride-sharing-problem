import GetData
import trip_merging
from HopperDistance import find_distance
WINDOW_SIZE_IN_MIN = 15
DELAY_TOLERANCE = 0.25

class MergedTrips:
	"""
	Represents a merged pair of trips
	"""
	def __init__(self, trip1, trip2, ):
		self.trip_list = []
		if(trip1 == trip2):
			raise Exception("Duplicate Trip")
		self.trip_list.append(trip1)
		self.trip_list.append(trip2)

	def add(self, trip_id):
		if(self.contains(trip_id)):
			raise Exception("Duplicate Trip")
		self.trip_list.append(trip_id)

	def contains(self, trip_id):
		return trip_id in self.trip_list

	def getCostGain(self):
		distance_mapping = {}
		for id in self.trip_list:
			trip = GetData.GetTripDetails(id)
			distance = trip_merging.getDistanceFromSource(trip.destination.latitude, trip.destination.longitude)
			distance_mapping[distance] = id
		if len(self.trip_list) == 2:
			return sum(list(distance_mapping)) * 0.2
		if len(self.trip_list) == 3:
			return sum(list(distance_mapping)) * 0.3

	def getDistanceGain(self):
		distance_mapping = {}
		for id in self.trip_list:
			trip = GetData.GetTripDetails(id)
			distance = trip_merging.getDistanceFromSource(trip.destination.latitude, trip.destination.longitude)
			distance_mapping[distance] = id
		ordered_trip_list = []
		for distance in sorted(list(distance_mapping)):
			ordered_trip_list.append(distance_mapping[distance])
		i = 0
		combined_trip_distance = sorted(list(distance_mapping))[0]
		while(i<2):
			trip1 = GetData.GetTripDetails(ordered_trip_list[i])
			trip2 = GetData.GetTripDetails(ordered_trip_list[i+1])
			distance_between_destinations = find_distance(trip1.destination.latitude, trip1.destination.longitude,
					trip2.destination.latitude, trip2.destination.longitude)[0]
			combined_trip_distance += distance_between_destinations
		normal_trip_distance = sum(list(distance_mapping))
		return normal_trip_distance - combined_trip_distance

	def getTripCount(self):
		return len(self.trip_list)

	def __str__(self):
		sorted_trip_list = sorted(self.trip_list)
		hashed_string = ""
		for trip in sorted_trip_list:
			hashed_string += str(trip).zfill(20)
		return hashed_string

	def __hash__(self):
		return str(self).__hash__()

	def __eq__(self, other):
		return sorted(self.trip_list) == sorted(other.trip_list)

	def __ne__(self, other):
		# Not strictly necessary, but to avoid having both x==y and x!=y
		# True at the same time
		return not(self == other)


class Trip:
	"""
	Represents the attributes of a trip
	"""
	def __init__(self, id, source, destination, pickup_time, dropoff_time, distance, trip_time):
		self.id = id
		self.source = source
		self.destination = destination
		self.pickup_time = pickup_time
		self.dropoff_time = dropoff_time
		self.distance = distance
		self.trip_time = trip_time


class Location:
	"""
	Represents the coordinates of a location
	"""
	def __init__(self, latitude, longitude):
		self.latitude = latitude
		self.longitude = longitude