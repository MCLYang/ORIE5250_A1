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

  
df = pd.read_csv("data2.txt",names=["Taxi ID","Datetime","Longitude","Latitude","Speed","Direction","Occupied","Other"])
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



import math 

def getLocation():
  cartesian_prod = list(product(range(num_taxi), range(num_taxi)))
  m3 = gp.Model('facility-location')
  select = m3.addVars(num_taxi, vtype=GRB.BINARY, name='Select')
  assign = m3.addVars(cartesian_prod, vtype=GRB.BINARY, name='Assign')
  m3.update()

  n = math.sqrt(num_taxi)
  dists = distance_dict.values()
  avg_d = sum(dists)/len(dists)
  op_cost = n*avg_d

  m3.setObjective(gp.quicksum(select[i]*op_cost for i in range(num_taxi)) + gp.quicksum(assign[(i,j)]*distance_dict[(i,j)] for i in range(num_taxi) for j in range(num_taxi)), GRB.MINIMIZE)
  m3.update()

  m3.addConstrs((assign[(i,j)] <= select[i] for i,j in cartesian_prod), name='Setup2ship')
  m3.addConstrs((gp.quicksum(assign[(i,j)] for i in range(num_taxi)) == 1 for j in range(num_taxi)), name='Demand')
  m3.update()
  return m3,select


location,select = getLocation()
location.optimize()

print("[Uncapacitated Facility Location Problem], data2")
for facility in select.keys():
    if (abs(select[facility].x) > 1e-6):
        print(f" Build a emergency supply kits at location {facility}.")

# end = time.time()

# print(f"Runtime of the program is {end - start}")

