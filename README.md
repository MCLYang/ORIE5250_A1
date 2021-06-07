# ORIE5250_A1
### 1.download the dataset under the root:
```
wget https://www.dropbox.com/s/99aml4pu5n7rxad/course_files_export.zip
unzip course_files_export.zip
```
### 2. Run python for each file:
##### Problem 1: Compute Distances
```
def Haversine(point1,point2):
  #point is formatted as (lamba,theta)
  lambda1, theta1 = point1
  lambda2, theta2 = point2
  r = 6371000
  d = 2*r*np.arcsin(np.sqrt(np.sin((theta2-theta1)/2)**2+np.cos(theta1)*np.cos(theta2)*np.sin((lambda2-lambda1)/2)**2))
  return d
```
##### Problem 2: K-Center
###### P2a: Use Gurobi for small dataset(K=5 amd k=10)
```
python p2a_gurobi_k5_k10.py
```
###### P2b Use Gurobi for big dataset(K=20)
```
python p2b_gurobi_k20.py
```
###### P2bc Use Greedy for big dataset(K=20) and evalutation
```
p2bc_greedy_k20.py
```

##### Problem 3: K-Medium
###### P2a: Use Gurobi for small dataset(K=5 amd k=10)
```
python p3a_gurobi_k5_k10.py
```
###### P2b Use Gurobi for big dataset(K=20)
```
python p3b_gurobi_k20.py
```
###### P2bc Use Greedy for big dataset(K=20) and evalutation
```
p3bc_greedy_k20.py
```
