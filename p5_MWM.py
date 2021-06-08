from datetime import datetime, timedelta
import pandas as pd
import numpy as np

from networkx.algorithms import bipartite
import networkx as nx
import pdb

def Haversine(point1,point2):
  #point is formatted as (lamba,theta)
  lambda1, theta1 = point1
  lambda2, theta2 = point2
  r = 6371000
  d = 2*r*np.arcsin(np.sqrt(np.sin((theta2-theta1)/2)**2+np.cos(theta1)*np.cos(theta2)*np.sin((lambda2-lambda1)/2)**2))
  return d

data3 = pd.read_csv("data3.txt",names=["Taxi ID","Datetime","Longitude","Latitude","Speed","Direction","Occupied","Other"])
# data3.set_index("Taxi ID")
# data3.sort_values(by=['Datetime'])

riders_set = data3[(data3['Datetime'] > '2009-09-01 08:00:00') & (data3['Datetime'] < '2009-09-01 08:05:00')]
riders_set.set_index("Taxi ID")
riders_set.sort_values(by=['Taxi ID','Datetime'])

taxis_set = data3[(data3['Datetime'] > '2009-09-01 07:55:00') & (data3['Datetime'] < '2009-09-01 08:00:00')]
taxis_set.set_index("Taxi ID")
taxis_set.sort_values(by=['Taxi ID','Datetime'])


def compute_cost(match,rider_dict,taxi_dict):
  cost = 0
  for key in match:
    d = Haversine(rider_dict[key],taxi_dict[match[key]])
    cost = cost + d
  return cost


def getRiders_taxis(riders_set,taxis_set):
  # Datetime = np.array(riders_set["Datetime"])
  # Longitude = np.array(riders_set["Longitude"])
  # Latitude = np.array(riders_set["Latitude"])
  # Occupied = np.array(riders_set["Occupied"])
  rider_dict = {}
  Taxi_ID = np.array(riders_set["Taxi ID"])
  id_set = set(Taxi_ID)
  for taxi_id in id_set:
    temp_set = riders_set[riders_set["Taxi ID"] == taxi_id]
    if np.array(temp_set['Occupied']).sum() != 0 and np.array(temp_set['Occupied']).sum() != len(np.array(temp_set['Occupied'])):
      # pdb.set_trace()
      length = len(np.array(temp_set['Occupied']))
      for i in range(length):
        if np.array(temp_set['Occupied'])[i] == 0:
          Longitude = np.array(temp_set['Longitude'])[i]
          Latitude = np.array(temp_set['Latitude'])[i]
          name = np.array(temp_set["Taxi ID"])[i]
          rider_dict[name] = (Longitude,Latitude)
          break

  taxi_dict = {}
  delete_keys = []
  for key in rider_dict:
    name = key
    temp_set = taxis_set[taxis_set["Taxi ID"] == name]
    length = len(temp_set)
    if length == 0:
      delete_keys.append(key)
    elif np.array(temp_set['Occupied']).sum() == 0:
      Longitude = np.array(temp_set['Longitude'])[0]
      Latitude = np.array(temp_set['Latitude'])[0]
      name = np.array(temp_set["Taxi ID"])[0]
      taxi_dict[name] = (Longitude,Latitude)
    elif np.array(temp_set['Occupied'])[-1] == 1:
      taxi_dict[name] = rider_dict[name]
    else:
      for i in range(length):
        j = length-i-1
        if np.array(temp_set['Occupied'])[j] == 1:
          k = j+1
          Longitude = np.array(temp_set['Longitude'])[k]
          Latitude = np.array(temp_set['Latitude'])[k]
          name = np.array(temp_set["Taxi ID"])[k]
          taxi_dict[name] = (Longitude,Latitude)

  for k in delete_keys:
    del rider_dict[k]

  # pdb.set_trace()
  return rider_dict,taxi_dict

print("=======Part A=======")
rider_dict,taxi_dict = getRiders_taxis(riders_set,taxis_set)
assert len(rider_dict) == len(taxi_dict)
print("=======Part B========")
names = list(rider_dict.keys())
B = nx.Graph()
B.add_nodes_from([name+"_rider" for name in names], bipartite=0)
B.add_nodes_from([name+"_taxi" for name in names], bipartite=1)
for r in rider_dict:
  for t in taxi_dict:
    d = Haversine(rider_dict[r],taxi_dict[t])
    B.add_edge(r+"_rider", t+"_taxi", weight = d)

rider_names = [name+"_rider" for name in names]
print("=======Part C=======")



match_original = {}
for name in names:
  match_original[name] = name

orginal_cost = compute_cost(match_original,rider_dict,taxi_dict)
print("original cost:",orginal_cost)
# pdb.set_trace()

#Part C
matching = bipartite.matching.minimum_weight_full_matching(B,top_nodes=rider_names)

algo_match = {}
for k in matching:
  if k[:-5] == "_rider":
    algo_match[k[:-5]] = matching[k][:-6]
# pdb.set_trace()
algo_cost = compute_cost(algo_match,rider_dict,taxi_dict)
print("algo cost: ",algo_cost)
print("difference: ",orginal_cost - algo_cost)

# pdb.set_trace()
# def getMatching():

#   gasLocations = getGasLocations()

#   taxiLocations = []
#   taxiDist = []
#   for index, point in data3.iterrows():
#     taxiDist.append((point['Latitude'],point['Longitude']))
#     taxiLocations.append(str(point['Latitude'])+"#"+str(point['Longitude']))

#   gasLocs = []
#   for gas in gasLocations:
#     gasLocs.append(str(gas[0])+"#"+str(gas[1]))
  
#   print("=======Part B========")

#   #Part B
#   B = nx.Graph()
#   B.add_nodes_from(taxiLocations, bipartite=0)
#   B.add_nodes_from(gasLocs, bipartite=1)

#   import pdb
#   pdb.set_trace()

  

#   for tax in taxiDist:
#     for gas in gasLocations:
#       d = Haversine(tax,gas)
#       B.add_edge(str(tax[0])+"#"+str(tax[1]), str(gas[0])+"#"+str(gas[1]), weight = d)

#   print("=======Part C=======")
#   #Part C
#   matching = bipartite.matching.minimum_weight_full_matching(B,top_nodes=taxiLocations)

#   return matching

# print(getMatching())
