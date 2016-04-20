import pickle
import input_file
import logging
#from GoogleDistance import find_distance
from HopperDistance import find_distance
import data_model
import networkx as nx
MERGING_TRESHOLD = 0.5
(SOURCE_LATITUDE, SOURCE_LONGITUDE) = (40.644104, -73.782665)

def find_distance_from_source(latitude, longitude):
	return find_distance(SOURCE_LATITUDE, SOURCE_LONGITUDE, latitude, longitude)

def get_shareability_graph(trips, treshold):
	graph_with_normal_treshold = nx.Graph()
	graph_with_restricted_treshold = nx.Graph()
	for i in range(len(trips)):
		for j in range(i, len(trips)):
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
				if(delay_for_b < treshold):
					graph_with_normal_treshold.add_nodes_from([trips[i].id, trips[j].id])
					graph_with_normal_treshold.add_edge((trips[i].id, trips[j].id), sharing_gain)
				if(delay_for_b < treshold/2):
					graph_with_restricted_treshold.add_nodes_from([trips[i].id, trips[j].id])
					graph_with_restricted_treshold.add_edge((trips[i].id, trips[j].id), sharing_gain)
			except Exception as e:
				pass
	return (graph_with_normal_treshold, graph_with_restricted_treshold)

def get_merged_trips(graph):
	list_of_merged_trips = []
	matched_edges = nx.algorithms.matching.max_weight_matching(graph)
	for i in matched_edges:
		trip1 = i
		trip2 = matched_edges[i]
		merged_trip = MergedTrip(trip1, trip2)
		list_of_merged_trips.append(merged_trip)
	return list_of_merged_trips

def remove_trips_from_graph(graph, list_of_merged_trips):
	graph_copy = copy.deepcopy(graph)
	for merged_trip in list_of_merged_trips:
		graph_copy.remove_edge(merged_trip.trip1, merged_trip.trip2);
	return graph_copy

def find_trip(list_of_merged_trips, trip):
	for merged_trip in list_of_merged_trips:
		if(merged_trip.contains(trip)):
			return merged_trip

def algorithm():
	logging.basicConfig(filename='distance.log')
	result_file = open('result_graph.p', 'wb')
	trip_subset = input_file.get_batch(0)
	graph_with_normal_treshold, graph_with_restricted_treshold = get_shareability_graph(trip_subset, MERGING_TRESHOLD)
	trips_merged_in_first_round = get_merged_trips(graph_with_normal_treshold)
	restricted_graph_with_edges_removed = remove_trips_from_graph(graph_with_restricted_treshold, trips_merged_in_first_round)
	merged_trips = get_merged_trips(restricted_graph_with_edges_removed)


if __name__ == "__main__":
	algorithm()

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