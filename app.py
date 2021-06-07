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

def get_data(data):
  df = pd.read_csv(data,names=["Taxi ID","Datetime","Longitude","Latitude","Speed","Direction","Occupied","Other"])
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
  return distance_dict,Longitude,Latitude,num_taxi



# distance_dict,Longitude,Latitude,num_taxi = get_data("data2.txt")
# K = 5
# cartesian_prod = list(product(range(num_taxi), range(num_taxi)))
# m = gp.Model('kits_location')
# select = m.addVars(num_taxi, vtype=GRB.BINARY, name='Select')
# assign = m.addVars(cartesian_prod, vtype=GRB.BINARY, name='Assign')
# z = m.addVar(vtype=GRB.CONTINUOUS, name='z')
# m.update()
# m.setObjective(z, GRB.MINIMIZE)
# m.update()
# m.addConstrs((gp.quicksum(assign[(i,j)]*distance_dict[(i,j)] for i in range(num_taxi)) <= z for j in range(num_taxi)), name='circle')
# m.addConstrs((assign[(i,j)] <= select[i] for i,j in cartesian_prod), name='Setup2ship')
# m.addConstrs((gp.quicksum(assign[(i,j)] for i in range(num_taxi)) == 1 for j in range(num_taxi)), name='Demand')
# m.addConstr((gp.quicksum(select[i] for i in range(num_taxi)))<=K, name='k_kits')
# m.update()
# m.optimize()

# print("[K-center],K = 5, data2")
# for facility in select.keys():
#     if (abs(select[facility].x) > 1e-6):
#         print(f" Build a emergency supply kits at location {facility}.")


# distance_dict,Longitude,Latitude,num_taxi = get_data("data2.txt")
# K = 10
# cartesian_prod = list(product(range(num_taxi), range(num_taxi)))
# m = gp.Model('kits_location')
# select = m.addVars(num_taxi, vtype=GRB.BINARY, name='Select')
# assign = m.addVars(cartesian_prod, vtype=GRB.BINARY, name='Assign')
# z = m.addVar(vtype=GRB.CONTINUOUS, name='z')
# m.update()
# m.setObjective(z, GRB.MINIMIZE)
# m.update()
# m.addConstrs((gp.quicksum(assign[(i,j)]*distance_dict[(i,j)] for i in range(num_taxi)) <= z for j in range(num_taxi)), name='circle')
# m.addConstrs((assign[(i,j)] <= select[i] for i,j in cartesian_prod), name='Setup2ship')
# m.addConstrs((gp.quicksum(assign[(i,j)] for i in range(num_taxi)) == 1 for j in range(num_taxi)), name='Demand')
# m.addConstr((gp.quicksum(select[i] for i in range(num_taxi)))<=K, name='k_kits')
# m.update()
# m.optimize()

# print("[K-center],K = 10, data2")
# for facility in select.keys():
#     if (abs(select[facility].x) > 1e-6):
#         print(f" Build a emergency supply kits at location {facility}.")



distance_dict,Longitude,Latitude,num_taxi = get_data("data1.txt")
K = 20
cartesian_prod = list(product(range(num_taxi), range(num_taxi)))
m = gp.Model('kits_location')
select = m.addVars(num_taxi, vtype=GRB.BINARY, name='Select')
assign = m.addVars(cartesian_prod, vtype=GRB.BINARY, name='Assign')
z = m.addVar(vtype=GRB.CONTINUOUS, name='z')
m.update()
m.setObjective(z, GRB.MINIMIZE)
m.update()
m.addConstrs((gp.quicksum(assign[(i,j)]*distance_dict[(i,j)] for i in range(num_taxi)) <= z for j in range(num_taxi)), name='circle')
m.addConstrs((assign[(i,j)] <= select[i] for i,j in cartesian_prod), name='Setup2ship')
m.addConstrs((gp.quicksum(assign[(i,j)] for i in range(num_taxi)) == 1 for j in range(num_taxi)), name='Demand')
m.addConstr((gp.quicksum(select[i] for i in range(num_taxi)))<=K, name='k_kits')
m.update()
m.optimize()

print("[K-center],K = 20, data1")
for facility in select.keys():
    if (abs(select[facility].x) > 1e-6):
        print(f" Build a emergency supply kits at location {facility}.")


