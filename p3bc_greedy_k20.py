import pandas as pd
import numpy as np
import gurobipy as gp
from gurobipy import GRB
from itertools import product

def Haversine(point1,point2):
  #point is formatted as (lamba,theta)
  lambda1, theta1 = point1
  lambda2, theta2 = point2
  r = 6371000
  d = 2*r*np.arcsin(np.sqrt(np.sin((theta2-theta1)/2)**2+np.cos(theta1)*np.cos(theta2)*np.sin((lambda2-lambda1)/2)**2))
  return d

def get_argmincost(V,S):
  mincost = 1e20
  mincost_idx = 0

  for i in range(len(V)):
    if i not in S:
      # suppose i is the canidate, compute the cost
      temp_S = []
      for k in S:
        temp_S.append(k)
      temp_S.append(i)
      cost = 0
      # iterate the rest of points which are not part of temp_S
      for j in range(len(V)):
        if j not in temp_S:
          d = 1e20
          for c in temp_S:
            d_temp = distance_dict[(c,j)]
            # assign each point to the closest neighboor
            if d_temp<d:
              d = d_temp
          cost = cost + d
      if cost < mincost:
        mincost = cost
        mincost_idx = i
  return mincost_idx

def k_median_greedy(V,k):
  # V is the set of points
  # return is S to store the center canidates. 
  num_points = len(V)
  init_idx = np.random.choice(num_points)
  init_point = V[init_idx]
  S = []
  S.append(init_idx)
  while len(S)<k:
    S.append(get_argmincost(V,S))
  return S
  
df = pd.read_csv("data1.txt",names=["Taxi ID","Datetime","Longitude","Latitude","Speed","Direction","Occupied","Other"])
Longitude = np.array(df["Longitude"],dtype=float)
Latitude = np.array(df["Latitude"],dtype=float)
num_taxi = len(Latitude)
# Construct the N*N adjcent matrix to store the pair-wise distance.
# I use the dictionary to store the the matrix
# key is the (i,j) then value is the corresponding distance
distance_dict = {}
for i in range(num_taxi):
  for j in range(num_taxi):
    idx = (i,j)
    point1 = [Longitude[i],Latitude[i]]
    point2 = [Longitude[j],Latitude[j]]
    d = Haversine(point1,point2)
    distance_dict[idx] = d

temp = np.array([Longitude,Latitude])
V = {}
for i in range(temp.shape[1]):
  V[i] = temp[:,i]


import time 
start = time.time()
locations_median = k_median_greedy(V,k=20)
end = time.time()
print(f"Runtime of the program is {end - start}")

def compute_cost(V,S,task = "k-center"):
  if task == "k-center":
    distance = []
    for taxi in V:
      if taxi not in S:
        d = 1e20
        for c in S:
          d_temp = distance_dict[(c,taxi)]
          if d_temp<d:
            d = d_temp
        distance.append(d)
    distance = np.array(distance)
    # print(len(distance))
    cost = np.min(distance)
    return cost
  if task == "k-median":
    distance = []
    for taxi in V:
      if taxi not in S:
        d = 1e20
        for c in S:
          d_temp = distance_dict[(c,taxi)]
          if d_temp<d:
            d = d_temp
        distance.append(d)
    distance = np.array(distance)
    # print(len(distance))
    cost = np.mean(distance)
    return cost

S = locations_median
print("k-median, Greedy Cost:",compute_cost(V,S = S,task = "k-median"))