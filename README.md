# "Point-cloud-interpolation"
Try project point to face (consists of points in .csv) along face normal or fixed vector

<p align="center">
<img src=https://github.com/Plus-1000/Point-cloud-interpolation/blob/main/pic/p0.jpg width="600" >
<b>
&nbsp;<br>
&nbsp;<br>
 
## Point interpolation along pt_cloud face normal
Suppose we have a point near pt_cloud, this method tries project the point on the "face" of point cloud along face normal

## 1, How the point cloud looks like
The pt_cloud consists of points with coordinates in CSV format.
<p align="center">
<img src=https://github.com/Plus-1000/Point-cloud-interpolation/blob/main/pic/p1.jpg width="600" >
<b>
&nbsp;<br>
&nbsp;<br>
 
## 2, About the points which will be projected onto pt_cloud "face"
Red color points are on the convex side, yellow point are ont the concave side. 

<p align="center">
<img src=https://github.com/Plus-1000/Point-cloud-interpolation/blob/main/pic/p2.jpg width="600" >
<b>
&nbsp;<br>
&nbsp;<br>
 
## 3, About the calculation: * Item 1
* Nearest points and face normal
* Rotete nearest pts and pt along the Z axis upward
* Interpolation calculation, get the distance from pt to grid
* Back to original 
&nbsp;<br>

 1), Find nearest points on pt_cloud and the point vector.
<p align="center">
<img src=https://github.com/Plus-1000/Point-cloud-interpolation/blob/main/pic/p3_1.jpg width="600" >
<b>
&nbsp;<br>
&nbsp;<br>

 
 2), Transfer point and it's nearest neighbors to new datum, then the local Z+ direction is straight upwards.
<p align="center">
<img src=https://github.com/Plus-1000/Point-cloud-interpolation/blob/main/pic/p3_2.jpg width="600" >
<b>
&nbsp;<br>
&nbsp;<br>
 
 3), Use scipy.interpolation.griddata, to get the distance from the point to face 
<p align="center">
<img src=https://github.com/Plus-1000/Point-cloud-interpolation/blob/main/pic/p3_1.jpg width="600" >
<b>
&nbsp;<br>
&nbsp;<br>
 
 4), Return to the original coordinate system, move the point along the opposite direction of the point vector, and save this point.
<p align="center">
<img src=https://github.com/Plus-1000/Point-cloud-interpolation/blob/main/pic/p3_1.jpg width="600" >
<b>
&nbsp;<br>
&nbsp;<br>
 
## 4, Check the result
<p align="center">
<img src=https://github.com/Plus-1000/Point-cloud-interpolation/blob/main/pic/p3_1.jpg width="600" >
<b>
&nbsp;<br>

## 5, Factors affecting interpolation accuracy:
* The number of points selected for interpolation
* The griddata method (‘linear’, ‘nearest’, ‘cubic’)
* Other factors (e.g., point cloud quality)
