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


