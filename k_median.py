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





def getKMedian(K):
  cartesian_prod = list(product(range(num_taxi), range(num_taxi)))
  m2 = gp.Model('k-median')
  select = m2.addVars(num_taxi, vtype=GRB.BINARY, name='Select')
  assign = m2.addVars(cartesian_prod, vtype=GRB.BINARY, name='Assign')
  m2.update()

  m2.setObjective(gp.quicksum(assign[(i,j)]*distance_dict[(i,j)] for i in range(num_taxi) for j in range(num_taxi)), GRB.MINIMIZE)
  m2.update()

  m2.addConstrs((assign[(i,j)] <= select[i] for i,j in cartesian_prod), name='Setup2ship')
  m2.addConstrs((gp.quicksum(assign[(i,j)] for i in range(num_taxi)) == 1 for j in range(num_taxi)), name='Demand')
  m2.addConstr((gp.quicksum(select[i] for i in range(num_taxi)))<=K, name='k_kits')
  m2.update()
  return m2,select

import pdb

#K=5
# k5,s5 = getKMedian(5)

#K=10
k20,s20 = getKMedian(20)

# k5.optimize()
# print("**********K-median,K==5,data2**********")
# for facility in s5.keys():
#     if (abs(s5[facility].x) > 1e-6):
#         print(f"Build a gas station at location {facility}.")


print("**********K-median,K==20,data1**********")
k20.optimize()
for facility in s20.keys():
    if (abs(s20[facility].x) > 1e-6):
        print(f" Build a gas station at location {facility}.")

