import logging
from HopperDistance import find_distance
import data_model
import GetData
import networkx as nx
import copy
import datetime

WALKING_TRESHOLD = 0
MERGING_TRESHOLD = 0.02
WINDOW_SIZE = 5
DATA_LIMIT = 200

(SOURCE_LATITUDE, SOURCE_LONGITUDE) = (40.644104, -73.782665)

def find_distance_from_source(latitude, longitude):
	return find_distance(SOURCE_LATITUDE, SOURCE_LONGITUDE, latitude, longitude)

def get_shareability_graph(trips, treshold):
	graph_with_normal_treshold = nx.Graph()
	graph_with_restricted_treshold = nx.Graph()
	for i in range(len(trips)):
		for j in range(i+1, len(trips)):
			try:
				trip_distance_i = find_distance_from_source(trips[i].destination.latitude, trips[i].destination.longitude)[0]
				trip_distance_j = find_distance_from_source(trips[j].destination.latitude, trips[j].destination.longitude)[0]
				distance_between_destinations = find_distance(trips[i].destination.latitude, trips[i].destination.longitude,
					trips[j].destination.latitude, trips[j].destination.longitude)[0]
				a, b = sorted([trip_distance_i, trip_distance_j])
				ab = distance_between_destinations
				distance_for_combined_trip = a + ab
				delay_for_b = (distance_for_combined_trip - b)/float(b)
				sharing_gain = distance_for_combined_trip/(a+b)
				walking = ab < WALKING_TRESHOLD
				if(delay_for_b < treshold):
					graph_with_normal_treshold.add_nodes_from([trips[i].id, trips[j].id])
					graph_with_normal_treshold.add_edge(trips[i].id, trips[j].id, weight=sharing_gain, delay=delay_for_b, walking=walking)
					#print "a:"+str(a)+"b:"+str(b)+"ab:"+str(ab)+"distance combined"+str(distance_for_combined_trip)+"\n"+"delay"+str(delay_for_b)+"\n"
				if(delay_for_b < treshold/2):
					graph_with_restricted_treshold.add_nodes_from([trips[i].id, trips[j].id])
					graph_with_restricted_treshold.add_edge(trips[i].id, trips[j].id, weight=sharing_gain, delay=delay_for_b, walking=walking)
			except Exception as e:
				pass
	return (graph_with_normal_treshold, graph_with_restricted_treshold)

def get_merged_trips(graph):
	list_of_merged_trips = {}
	matched_edges = nx.algorithms.matching.max_weight_matching(graph)
	#print matched_edges
	for i in matched_edges:
		#print(str(i) + ":" + str(matched_edges[i]))
		trip1 = i
		trip2 = matched_edges[i]
		list_of_merged_trips[data_model.MergedTrips(trip1, trip2, )] = {"sharing_gain": graph[trip1][trip2]["weight"], "delay": graph[trip1][trip2]["delay"], "walking": graph[trip1][trip2]["walking"]}
	return list(list_of_merged_trips)

def remove_tripshare_from_graph(graph, list_of_merged_trips):
	graph_copy = copy.deepcopy(graph)
	for merged_trip in list_of_merged_trips:
		try:
			graph_copy.remove_edge(merged_trip.trip_list[0], merged_trip.trip_list[1])
		except Exception as e:
			pass
	return graph_copy

def remove_trips_from_graph(graph, list_of_merged_trips):
	graph_copy = copy.deepcopy(graph)
	for merged_trip in list_of_merged_trips:
		try:
			graph_copy.remove_node(merged_trip)
		except Exception as e:
			pass
	return graph_copy

def remove_redundant_edges(graph, list_of_trips):
	graph_copy = copy.deepcopy(graph)
	for i in range(len(list_of_trips)):
		for j in range(i+1, len(list_of_trips)):
			try:
				graph_copy.remove_edge(list_of_trips[i], list_of_trips[j])
			except Exception as e:
				pass
	return graph_copy

def prepare_graph(graph, list_of_trips_of_high_degree, list_of_double_trips):
	graph = remove_trips_from_graph(graph, list_of_trips_of_high_degree)
	return remove_redundant_edges(graph, list_of_double_trips)

def lone_trips(list_of_merged_trips):
	lone_trips_list = []
	all_trips = GetData.GetData(WINDOW_SIZE, DATA_LIMIT)
	for trip in all_trips:
		flag = True
		for merged_trip in list_of_merged_trips:
			if(merged_trip.contains(trip.id)):
				flag = False
				break
		if flag:
			lone_trips_list.append(trip.id)
	return lone_trips_list

def is_alrady_merged(list_of_merged_trips, trip):
	for merged_trip in list_of_merged_trips:
		if(merged_trip.contains(trip)):
			return len(merged_trip.trip_list) < 3
	return True

def find_trip(list_of_merged_trips, trip):
	for merged_trip in list_of_merged_trips:
		if(merged_trip.contains(trip)):
			if(len(merged_trip.trip_list) <= 2):
				return merged_trip

def add_trip_to_candidate(list_of_merged_trips, merged_trip):
	try:
		#print "Merged Trip: " + str(merged_trip)
		primary_merged_trip1 = find_trip(list_of_merged_trips, merged_trip.trip_list[0])
		primary_merged_trip2 = find_trip(list_of_merged_trips, merged_trip.trip_list[1])

		if primary_merged_trip1 and primary_merged_trip2:
			#print "Primary Merged Trip 1: " + str(primary_merged_trip1) + "Primary Merged Trip 2: " + str(primary_merged_trip2)
			primary_merged_trip1.add(primary_merged_trip2.trip_list[0])
			primary_merged_trip1.add(primary_merged_trip2.trip_list[1])
			list_of_merged_trips.pop(list_of_merged_trips.index(primary_merged_trip2))
			return merged_trip

		elif primary_merged_trip1:
			#print "Primary Merged Trip 1: " + str(primary_merged_trip1)
			if is_alrady_merged(list_of_merged_trips, merged_trip.trip_list[1]):
				primary_merged_trip1.add(merged_trip.trip_list[1])
			return primary_merged_trip1

		elif primary_merged_trip2:
			#print "Primary Merged Trip 2: " + str(primary_merged_trip2)
			if is_alrady_merged(list_of_merged_trips, merged_trip.trip_list[0]):
				primary_merged_trip2.add(merged_trip.trip_list[0])
			return primary_merged_trip2
	except Exception as e:
		raise e

def algorithm():
	logging.basicConfig(filename='distance.log')
	result_file = open('result_graph.p', 'wb')
	trip_subset = GetData.GetData(WINDOW_SIZE, DATA_LIMIT)
	graph_with_normal_treshold, graph_with_restricted_treshold = get_shareability_graph(trip_subset, MERGING_TRESHOLD)
	trips_merged_in_first_round = get_merged_trips(graph_with_normal_treshold)
	#print "First Round"
	#for i in trips_merged_in_first_round:
	#print "First len: " + str(len(trips_merged_in_first_round))
	restricted_graph_with_edges_removed = remove_tripshare_from_graph(graph_with_restricted_treshold, trips_merged_in_first_round)

	merged_trips = get_merged_trips(restricted_graph_with_edges_removed)
	print "Merged Trips"
	for merged_trip in merged_trips:
		add_trip_to_candidate(trips_merged_in_first_round, merged_trip)

	#print "Three trips"
	actualCost = 0.0
	combinedCost = 0.0
	actualDist = 0.0
	combinedDist = 0.0
	cost = 0.0
	tripCost = 0.0
	dist = 0.0
	tripDist = 0.0
	four_trips = 0
	three_trips = 0
	two_trips = 0
	list_of_trips_of_high_degree = []
	list_of_double_tripids = []
	list_of_double_trips = []
	single_trips = lone_trips(trips_merged_in_first_round)
	for trip in single_trips:
		print trip
	for i in trips_merged_in_first_round:
		#print str(i)
		print i.trip_list
		if len(i.trip_list) == 2:
			two_trips += 1
			list_of_double_trips.append(copy.deepcopy(i))
			for tId in i.trip_list:
				list_of_double_tripids.append(tId)
		elif len(i.trip_list) == 3:
			three_trips += 1
			for tId in i.trip_list:
				list_of_trips_of_high_degree.append(tId)
			list_of_trips_of_high_degree.append(i.trip_list)
		elif len(i.trip_list) == 4:
			four_trips += 1
			for tId in i.trip_list:
				list_of_trips_of_high_degree.append(tId)

		actualCost, combinedCost = i.getCostGain()
		actualDist, combinedDist = i.getDistanceGain()
		cost = cost + actualCost
		tripCost = tripCost + combinedCost
		dist = dist + actualDist
		tripDist = tripDist + combinedDist
	#graph_for_three_trips = prepare_graph(graph_with_restricted_treshold, list_of_trips_of_high_degree, list_of_double_tripids)
	#merged_trips = get_merged_trips(graph_for_three_trips)
	#for merged_trip in merged_trips:
	#	add_trip_to_candidate(list_of_double_trips, merged_trip)
	#for three in list_of_double_trips:
	#	print three
	print "Actual distance: %d" %dist
	print "Combined distance: %d" %tripDist
	print "Actual Cost: %d" %cost
	print "Combined Cost: %d" %tripCost
	print "four_trips: %d" %four_trips
	print "two trips: %d" %two_trips
	print "three_trips: %d" %three_trips







if __name__ == "__main__":
	tic = datetime.datetime.now()
	algorithm()
	toc = datetime.datetime.now()
	print toc - tic

"""
try:
	for i in range(30):
		for j in range(i, 30):
			(distance_between_sources, time_between_sources) = find_distance(
				str(trip_subset[i].source.latitude), str(trip_subset[i].source.longitude),
				str(trip_subset[j].source.latitude), str(trip_subset[j].source.longitude))
			(distance_for_a, time_for_a) = find_distance(
				str(trip_subset[i].source.latitude), str(trip_subset[i].source.longitude),
				str(trip_subset[i].destination.latitude), str(trip_subset[i].destination.longitude))
			(distance_for_b, time_for_b) = find_distance(
				str(trip_subset[j].source.latitude), str(trip_subset[j].source.longitude),
				str(trip_subset[j].destination.latitude), str(trip_subset[j].destination.longitude))
			(distance_form_a_to_b, time_form_a_to_b) = find_distance(
				str(trip_subset[i].source.latitude), str(trip_subset[i].source.longitude),
				str(trip_subset[j].destination.latitude), str(trip_subset[j].destination.longitude))
			(distance_form_b_to_a, time_form_b_to_a) = find_distance(
				str(trip_subset[j].source.latitude), str(trip_subset[j].source.longitude),
				str(trip_subset[i].destination.latitude), str(trip_subset[i].destination.longitude))
			(distance_between_destinations, time_between_destinations) = find_distance(
				str(trip_subset[i].destination.latitude), str(trip_subset[i].destination.longitude),
				str(trip_subset[j].destination.latitude), str(trip_subset[j].destination.longitude))
			configuration_distances = [
			(distance_between_sources + distance_for_a,
				distance_between_sources + distance_for_a + distance_between_destinations,
				distance_between_sources + distance_for_a + distance_between_destinations),
			(distance_between_sources + distance_for_b + distance_between_destinations,
				distance_between_sources + distance_for_b,
				distance_between_sources + distance_for_b + distance_between_destinations),
			(distance_between_sources + distance_form_a_to_b + distance_between_destinations,
				distance_between_sources + distance_form_a_to_b,
				distance_between_sources + distance_form_a_to_b + distance_between_destinations),
			(distance_between_sources + distance_form_b_to_a,
				distance_between_sources + distance_form_b_to_a + distance_between_destinations,
				distance_between_sources + distance_form_b_to_a + distance_between_destinations)
				]
			shareable = True in [(effective_distance_a-distance_for_a)/distance_for_a < 0.25 and (effective_distance_b-distance_for_b)/distance_for_b < 0.25 for effective_distance_a, effective_distance_b, distance in configuration_distances]

			if shareable:
				trip_gain = float(distance)/float(distance_for_a + distance_for_b)
				graph.add_edge((trip_subset[i].id, trip_subset[j].id), trip_gain)
				for effective_distance_a, effective_distance_b, distance in configuration_distances:
					logging.error('shareable loss(a): %f loss(b):%f',
						(effective_distance_a-distance_for_a)/distance_for_a,
						(effective_distance_b-distance_for_b)/distance_for_b)
			else:
				for effective_distance_a, effective_distance_b, distance in configuration_distances:
					logging.error('loss(a): %f loss(b):%f',
						(effective_distance_a-distance_for_a)/distance_for_a,
						(effective_distance_b-distance_for_b)/distance_for_b)
except Exception as e:
	logging.error(str(e))
#graph.add_nodes_from([trip.id for trip in trip_subset])
pickle.dump(graph, result_file)
"""