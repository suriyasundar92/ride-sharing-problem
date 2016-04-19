WINDOW_SIZE_IN_MIN = 15
DELAY_TOLERANCE = 0.25

class MergedTrips:
	"""
	Represents a merged pair of trips
	"""
	def __init__(self, trip1, trip2):
		self.trip_list = []
		if(trip1.id == trip2.id):
			raise Exception("Duplicate Trip")
		self.trip_list.append(trip1.id)
		self.trip_list.append(trip2.id)

	def add(trip):
		if(self.contains(trip.id)):
			raise Exception("Duplicate Trip")
		self.trip_list.append(trip)

	def contains(trip):
		return trip.id in self.trip_list


class Trip:
	"""
	Represents the attributes of a trip
	"""
	def __init__(self, id, source, destination, pickup_time, dropoff_time):
		self.id = id
		self.source = source
		self.destination = destination
		self.pickup_time = pickup_time
		self.dropoff_time = dropoff_time


class Location:
	"""
	Represents the coordinates of a location
	"""
	def __init__(self, latitude, longitude):
		self.latitude = latitude
		self.longitude = longitude
