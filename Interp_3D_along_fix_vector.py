import pandas as pd
import numpy as np
import os
import sys
from sklearn.neighbors import NearestNeighbors
from scipy.interpolate import griddata
global curr_path, vec2
curr_path = os.getcwd()+'\\' 
vec2=[0,0,1] # pt interpolation require the Z axis upwards

# find cloest points along nomal in dia "D1"
def nearestPT_along_normal(pts, pt, vec1):
    D1=1.5
    points=pts
    reference_point = pt  # Point 
    direction_vector = vec1  # Vector 
    diameter = D1
    radius = diameter / 2

    # Calculate points relative to the reference point
    points_centered = points - reference_point

    # Project points onto the direction vector
    projections = np.dot(points_centered, vec1)

    # Calculate the squared distance of projections to the reference point
    distances_squared = np.sum((points_centered - projections[:, np.newaxis] * vec1) ** 2, axis=1)
    radius_squared = radius ** 2

    # Filter points within the radius
    within_radius = distances_squared <= radius_squared
    filtered_points = points[within_radius]
    
    return(filtered_points)

def normalize_vector(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def rotation_matrix_between_vectors(vec1, vec2):
    # Find the rotation matrix that aligns vec1 to vec2
    a, b = normalize_vector(vec1), normalize_vector(vec2)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    
    I = np.identity(3)
    if s == 0:
        if c > 0:
            return I
        else:
            return -I

    v_cross = np.array([
        [0, -v[2], v[1]],
        [v[2], 0, -v[0]],
        [-v[1], v[0], 0]
    ])

    R = I + v_cross + np.dot(v_cross, v_cross) * ((1 - c) / (s ** 2))
    return R

def transfer_point(point, vec1, vec2):
    rotation_mat = rotation_matrix_between_vectors(vec1, vec2)
    transferred_point = np.dot(rotation_mat, point)
    return transferred_point

# point cloud interpolation
def pt_interp(pt_cloud, pt): # return distance from point to point clouds in Z direction
    X = pt_cloud[:, 0]
    Y=pt_cloud[:, 1]
    Z=pt_cloud[:, 2]
    xi=pt[0]
    yi=pt[1]
    zi = griddata((X, Y), Z, (xi, yi), method='cubic')
    dist=zi-pt[2]
    # print('dist:  ==========', dist)
    return dist
    
# move point at a distance along vector 
def move_point_along_vector(point, vector, distance):
    norm_vector = vector / np.linalg.norm(vector) # Normalize the vector
    scaled_vector = norm_vector * distance # Scale the normalized vector by the distance
    new_point = point + scaled_vector # Move the point by adding the scaled vector
    return new_point


# sub entry (point cloud on new face, points on idel face, number of nearest point for interpolation)
def one_point_interp(pt_cloud, pt, vec1): # k number of points involoved in interpolation

    # Generate cloest_points and vector
    nearest_pts=nearestPT_along_normal(pt_cloud,pt, vec1) # pts_ijk[0]: nearest_points, pts_ijk[1]: vector 
    print('nearest_pts: ',nearest_pts)
    np.savetxt(curr_path+'\\pts\\' + 'nearest_pts.csv', nearest_pts, delimiter = ",")
    
    # transfer nearest points to new vector direction, the Z+ (vec2)
    temp_list=[]
    for each_pt in nearest_pts:
        j=transfer_point(each_pt, vec1, vec2)
        temp_list.append(j.tolist())
    transfered_pts=np.array(temp_list)
    print('transfered_pts: ', transfered_pts)
    np.savetxt(curr_path+'\\pts\\' + 'transfered_pts.csv', transfered_pts, delimiter = ",")

    # transfer single point (or orginal face) to new vector direction Z+ (vec2)
    transfered_pt=transfer_point(pt, vec1, vec2)
    print('transfered_pt: ', transfered_pt)
    np.savetxt(curr_path+'\\pts\\' + 'transfered_pt.csv', transfered_pt, delimiter = ",")
    
    # check distance from point on idel face to new face along face vector
    Dist=pt_interp(transfered_pts, transfered_pt)
    print('Dist: ', Dist)

    # move point along vector, will copy point on idel face to deformed face along vector
    new_pt=move_point_along_vector(pt, vec1, Dist)
    
    # print('new_pt======================', new_pt, type(new_pt))
    return new_pt

# ======  Main() ================
if __name__=='__main__':
    k=25 # number of points involoved in interpolation
    # vec1=[2.903868880,-2.546656479,1.518528619] # fixed vector
    vec1=[-11,0.1,0.1] # about same as X axis
    print(vec1)
    vec1= vec1/np.linalg.norm(vec1)
    print(vec1)
    
    df = pd.read_csv(curr_path+'\\pts\\'+'pts_cloud.csv', header=None) # no noisy reduction
    pt_cloud = df.values # 将点云数据转换为numpy数组

    df = pd.read_csv(curr_path+'\\pts\\' + 'pt_input.csv', header=None) # no noisy reduction
    pt_input = df.values # 将点云数据转换为numpy数组

    # interp loop
    interp_list=[]
    for each_p in pt_input:
        interp_p=one_point_interp(pt_cloud, each_p, vec1)
        interp_list.append(interp_p.tolist())
    interped_pts=np.array(interp_list)

    df=pd.DataFrame(interped_pts)
    print(df)
    
    df.to_csv(curr_path+'\\pts\\' +'pt_output_interp_along_fix_vector.csv', index=False, header=None)


