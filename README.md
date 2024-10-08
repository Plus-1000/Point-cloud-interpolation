# "Point-cloud-interpolation"
Try projecting the point onto the face (which consists of points in a .csv file) along the face normal or a fixed vector, or find the closest point from pt_cloud

<p align="center">
<img src=https://github.com/Plus-1000/Point-cloud-interpolation/blob/main/pic/p0.jpg width="600" >
<b>
&nbsp;<br>
&nbsp;<br>
 
## Point interpolation along pt_cloud face normal
Suppose we have a point near pt_cloud, this method tries to project the point on the "face" of the point cloud along the face normal

## 1, How the point cloud looks like
The pt_cloud consists of points with coordinates in CSV format.
<p align="center">
<img src=https://github.com/Plus-1000/Point-cloud-interpolation/blob/main/pic/p1.jpg width="600" >
<b>
&nbsp;<br>
&nbsp;<br>
 
## 2, About the points which will be projected onto pt_cloud "face"
Red color points are on the convex side, yellow points are on the concave side. 

<p align="center">
<img src=https://github.com/Plus-1000/Point-cloud-interpolation/blob/main/pic/p2.jpg width="600" >
<b>
&nbsp;<br>
&nbsp;<br>
 
## 3, About the calculation: 
* Nearest points and face normal
* Rotate the datum and the involved points, ensuring the Z+ direction remains straight and upward
* Interpolation calculation, get the distance from pt to grid
* Back to original 
&nbsp;<br>

 1), Find nearest points on pt_cloud and the point vector.
<p align="center">
<img src=https://github.com/Plus-1000/Point-cloud-interpolation/blob/main/pic/p3_1.jpg width="600" >
<b>
&nbsp;<br>
&nbsp;<br>

 
 2), Transfer point and it's nearest neighbors to new datum, which's Z+ direction is straight upwards.
<p align="center">
<img src=https://github.com/Plus-1000/Point-cloud-interpolation/blob/main/pic/p3_2.jpg width="600" >
<b>
&nbsp;<br>
&nbsp;<br>
 
 3), Use scipy.interpolation.griddata, to get the distance from the point to face 
<p align="center">
<img src=https://github.com/Plus-1000/Point-cloud-interpolation/blob/main/pic/p3_3.jpg width="600" >
<b>
&nbsp;<br>
&nbsp;<br>
 
 4), Return to the original datum, we move the point in the opposite direction of its vector by the previously calculated distance, resulting in the interpolated point.
<p align="center">
<img src=https://github.com/Plus-1000/Point-cloud-interpolation/blob/main/pic/p3_4.jpg width="600" >
<b>
&nbsp;<br>
&nbsp;<br>
 
## 4, Check the result
<p align="center">
<img src=https://github.com/Plus-1000/Point-cloud-interpolation/blob/main/pic/p4.jpg width="600" >
<b>
&nbsp;<br>
&nbsp;<br>
 
## 5, Factors affecting interpolation accuracy:
* The number of points (selected to proceed with interpolation)
* The griddata parameter (‘linear’, ‘nearest’, ‘cubic’)
* Other factors (e.g., point cloud quality)
&nbsp;<br>
&nbsp;<br>

## 6, Point interpolation along fixed vector
Please check: Interp_3D_along_fix_vector.py
&nbsp;<br>
&nbsp;<br>

## 7, Find the closest point from pt_cloud
Please check: Interp_3D_closest.py
&nbsp;<br>
&nbsp;<br>



*Wang Jian, 2024 Jun 12, wjian88@gmail.com*
