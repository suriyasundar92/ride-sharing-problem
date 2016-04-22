import GetData
import trip_merging
from HopperDistance import find_distance
WINDOW_SIZE_IN_MIN = 15
DELAY_TOLERANCE = 0.25
WALKING_TOLRENCE = 1.5

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
		combined_cost = 0.0
		for id in self.trip_list:
			trip = GetData.GetTripDetails(id)
			distance = trip_merging.find_distance_from_source(trip.destination.latitude, trip.destination.longitude)[0]
			distance_mapping[distance] = id
		sum_distance = sum(list(distance_mapping))
		if len(self.trip_list) == 2:
			combined_cost = sum_distance * 0.8
		elif len(self.trip_list) == 3:
			combined_cost = sum_distance * 0.7
		elif len(self.trip_list) == 4:
			combined_cost = sum_distance * 0.6

		return(sum_distance, combined_cost)


	def getDistanceGain(self):
		distance_mapping = {}
		ordered_trip_list = []
		for id in self.trip_list:
			trip = GetData.GetTripDetails(id)
			distance = trip_merging.find_distance_from_source(trip.destination.latitude, trip.destination.longitude)[0]
			distance_mapping[distance] = id
		for distance in sorted(list(distance_mapping)):
			ordered_trip_list.append(distance_mapping[distance])

		trip = GetData.GetTripDetails(ordered_trip_list[0])
		combined_trip_distance = trip.distance
		i=1
		source = 0
		while(i<len(self.trip_list)):
			trip1 = GetData.GetTripDetails(ordered_trip_list[source])
			trip2 = GetData.GetTripDetails(ordered_trip_list[i])
			difference = find_distance(trip1.destination.latitude, trip1.destination.longitude,
					trip2.destination.latitude, trip2.destination.longitude)[0]
			if difference > WALKING_TOLRENCE:
				source = i
				combined_trip_distance += difference
			else:
				print "nope: %s" %difference
			i += 1
		normal_trip_distance = sum(list(distance_mapping))
		return (normal_trip_distance, combined_trip_distance)

	def getPartner(self, id):
		for i in self.trip_list:
			if i != id:
				return i

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