# Point-cloud-interpolation
Try project point to face (pt cloud, coordinate in csv) along face normal or fixed vector

<p align="center">
<img src=https://github.com/Plus-1000/Point-cloud-interpolation/blob/main/pic/p0.jpg width="600" >
<b>


# Point interpolation along pt_cloud face normal
Suppose we a point near pt_cloud, this method tries project the point on the "face" of point cloud 

## 1, How the point cloud looks like
The pt_cloud consists of points with coordinates in CSV format.



&nbsp;<br>

## 2, About the points which will be projected onto pt_cloud "face"
Red color points are on the convex side, yellow point are ont the concave side. 

![Alt text](image-13.png)
&nbsp;<br>

## 3, About the calculation: * Item 1
* Nearest points and face normal
* Rotete nearest pts and pt along the Z axis upward
* Interpolation calculation, get the distance from pt to grid
* Back to original 



&nbsp;<br>
 1), Find nearest points on pt_cloud and the point vector.
![Alt text](image-14.png)


 
 2), Transfer point and it's nearest neighbors to new datum, then the local Z+ direction is straight upwards.
![Alt text](image-15.png)
 
 3), Use scipy.interpolation.griddata, to get the distance from the point to face 
![Alt text](image-17.png)
  
 4), Return to the original coordinate system, move the point along the opposite direction of the point vector, and save this point.
![Alt text](image-18.png)
 
## 4, Check the result
![Alt text](image-19.png)

## 5, Factors affecting interpolation accuracy:
* The number of points selected for interpolation
* The griddata method (‘linear’, ‘nearest’, ‘cubic’)
* Other factors (e.g., point cloud quality)
