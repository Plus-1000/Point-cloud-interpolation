# pip install pandas numpy scipy scikit-learn
# last version tested on 2024.Aug.02
import pandas as pd
import numpy as np
import os
import sys
from sklearn.neighbors import NearestNeighbors
from scipy.interpolate import griddata
global curr_path, vec2
curr_path = os.getcwd()+'\\' 
vec2=[0,0,1] # pt interpolation require the Z axis upwards

#0 test sub 
def test():
    return curr_path

# Get given pt, from pt_cloud find nearest_points 
def nearestPT(pt_cloud,pt,k):     # k 定义最近邻居的数量, 可以根据需要调整这个数值
    point_A = np.array(pt)
    nbrs = NearestNeighbors(n_neighbors=k, algorithm='auto').fit(pt_cloud)  # 初始化NearestNeighbors算法
    distances, indices = nbrs.kneighbors([point_A])   # 找到目标点A的k个最近邻居
    nearest_points = pt_cloud[indices[0]] # nearest points generated
    
    # Generate cloest_points and vector
    print('nearest_pts: ',nearest_points)
    np.savetxt(curr_path+'\\pts\\' + 'nearest_pts.csv', nearest_points, delimiter = ",")
    return  nearest_points
      
# from pt_cloud find the vector toward pt 
def _IJK(pts):   
     # 计算局部平面的法向量（PCA方法）
    mean_point = np.mean(pts, axis=0)
    cov_matrix = np.cov(pts - mean_point, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    normal_vector = eigenvectors[:, 0]  # 法向量是对应最小特征值的特征向量
    return  normal_vector

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
def one_point_interp(pt_cloud, pt, k): # k number of points involoved in interpolation

    # Generate cloest_points and vector
    nearest_pts=nearestPT(pt_cloud,pt,k) # pts_ijk[0]: nearest_points, pts_ijk[1]: vector 
    
    # Generate cloest_points and vector
    vec1=_IJK(nearest_pts) # pts_ijk[0]: nearest_points, pts_ijk[1]: vector 

    # transfer nearest points to new vector direction, the Z+ (vec2)
    temp_list=[]
    for each_pt in nearest_pts:
        j=transfer_point(each_pt, vec1, vec2)
        temp_list.append(j.tolist())
    transfered_pts=np.array(temp_list)
    # print(transfered_pts)

    # transfer single point (or orginal face) to new vector direction Z+ (vec2)
    transfered_pt=transfer_point(pt, vec1, vec2)
    
    # check distance from point on idel face to new face along face vector
    Dist=pt_interp(transfered_pts, transfered_pt)

    # move point along vector, will copy point on idel face to deformed face along vector
    new_pt=move_point_along_vector(pt, vec1, Dist)
    
    # print('new_pt======================', new_pt, type(new_pt))
    return new_pt

# ======  Main() ================
if __name__=='__main__':
    k=25 # number of points involoved in interpolation
    
    df = pd.read_csv(curr_path+'\\pts\\'+'pts_cloud.csv', header=None) # no noisy reduction
    pt_cloud = df.values # 将点云数据转换为numpy数组

    df = pd.read_csv(curr_path+'\\pts\\' + 'pt_input.csv', header=None) # no noisy reduction
    pt_input = df.values # 将点云数据转换为numpy数组

    # interp loop
    interp_list=[]
    for each_p in pt_input:
        interp_p=one_point_interp(pt_cloud, each_p, k)
        interp_list.append(interp_p.tolist())
    interped_pts=np.array(interp_list)

    df=pd.DataFrame(interped_pts)
    df.to_csv(curr_path+'\\pts\\' +'pt_output_interp_along_face_normal.csv', index=False, header=None)


