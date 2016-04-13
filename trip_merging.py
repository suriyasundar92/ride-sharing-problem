import pickle
import input_file
import logging
from GoogleDistance import find_distance
import data_model
import networkx as nx
logging.basicConfig(filename='distance.log')
result_file = open('result_graph.p', 'wb')
trip_subset = input_file.get_batch(0)[:30]
graph = nx.Graph()
graph.add_nodes_from([trip.id for trip in trip_subset])
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

pickle.dump(graph, result_file)
