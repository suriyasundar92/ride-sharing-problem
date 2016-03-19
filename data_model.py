WINDOW_SIZE_IN_MIN = 15

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
