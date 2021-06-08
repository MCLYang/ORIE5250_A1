from datetime import datetime, timedelta
import pandas as pd
import numpy as np

from networkx.algorithms import bipartite
import networkx as nx

def Haversine(point1,point2):
  #point is formatted as (lamba,theta)
  lambda1, theta1 = point1
  lambda2, theta2 = point2
  r = 6371000
  d = 2*r*np.arcsin(np.sqrt(np.sin((theta2-theta1)/2)**2+np.cos(theta1)*np.cos(theta2)*np.sin((lambda2-lambda1)/2)**2))
  return d

data3 = pd.read_csv("data3.txt",names=["Taxi ID","Datetime","Longitude","Latitude","Speed","Direction","Occupied","Other"])
data3.set_index("Taxi ID")
data3.sort_values(by=['Datetime'])

riders = data3[(data3['Datetime'] > '2009-09-01 08:00:00') & (data3['Datetime'] < '2009-09-01 08:05:00')]
riders.set_index("Taxi ID")
riders.sort_values(by=['Datetime'])

taxis = data3[(data3['Datetime'] > '2009-09-01 07:55:00') & (data3['Datetime'] < '2009-09-01 08:00:00')]
taxis.set_index("Taxi ID")
taxis.sort_values(by=['Datetime'])

def getRiderLocations():
  locations = []
  largeTaxis = []
  current_occ = {}
  ids = set()
  print("=======Part A=======")
  #Part A-1
  for index, point in riders.iterrows():
    id = point['Taxi ID']
    loc = tuple((point['Latitude'],point['Longitude']))
    occ = point['Occupied']
    dt = point['Datetime']
    if id in current_occ and current_occ[id] == 0 and occ == 1 and id not in ids:
      locations.append(loc)
      ids.add(id)
      #Part A-2
      prev_dt_1 = pd.to_datetime(dt) - pd.Timedelta(minutes=4, seconds=30)
      prev_dt_2 = pd.to_datetime(dt) - pd.Timedelta(minutes=5, seconds=30)
      taxi = taxis[(taxis['Taxi ID']==id) & (taxis['Datetime'] < str(prev_dt_1)) & (taxis['Datetime'] > str(prev_dt_2))].tail(1)
      if not taxi['Occupied'].all():
        largeTaxis.append(tuple((taxi['Latitude'],taxi['Longitude'])))
      else:
        t = data3[(data3['Taxi ID']==id) & (data3['Datetime'] > str(taxi['Datetime']))]
        t.sort_values(by=['Datetime'])
        for index, tax in t.iterrows():
          if tax['Occupied'] == 0:
            largeTaxis.append(tuple((tax['Latitude'],tax['Longitude'])))
            
    current_occ[id] = occ
  return locations, largeTaxis

def getMatching():

  gasLocations,taxiLocations = getRiderLocations()

  taxLocs = []
  for tax in taxiLocations:
    taxLocs.append(str(tax[0])+"#"+str(tax[1]))

  gasLocs = []
  for gas in gasLocations:
    gasLocs.append(str(gas[0])+"#"+str(gas[1]))
  
  print("=======Part B========")

  #Part B
  B = nx.Graph()
  B.add_nodes_from(taxLocs, bipartite=0)
  B.add_nodes_from(gasLocs, bipartite=1)
      
  for tax in taxiLocations:
    for gas in gasLocations:
      d = Haversine(tax,gas)
      B.add_edge(str(tax[0])+"#"+str(tax[1]), str(gas[0])+"#"+str(gas[1]), weight = d)

  print("=======Part C=======")

  #Part C
  matching = bipartite.matching.minimum_weight_full_matching(B,top_nodes=taxiLocations)

  return matching

print(getMatching())