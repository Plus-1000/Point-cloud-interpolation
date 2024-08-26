# Tested on Jun 25
# pip install pandas numpy scipy scikit-learn
import pandas as pd
import numpy as np
import os
import sys
from sklearn.neighbors import NearestNeighbors
global curr_path, vec2
curr_path = os.getcwd()+'\\' 

def one_point_cloest(pt_cloud,pt_in, k):
    # 定义目标点A的坐标（替换为实际的坐标）
    point_A = np.array(pt_in)
  
    # k = 1  定义最近邻居的数量, find one nearest point
    nbrs = NearestNeighbors(n_neighbors=k, algorithm='auto').fit(pt_cloud)  # 初始化NearestNeighbors算法
    distances, indices = nbrs.kneighbors([point_A])  # 找到目标点A的k个最近邻居
    pt_out = (pt_cloud[indices[0]]).flatten()
    return pt_out


if __name__=='__main__':
    k=15 # number of points involoved in interpolation
    df = pd.read_csv(curr_path+'\\pts\\'+'pts_cloud.csv', header=None) 
    pt_cloud = df.values 
    df = pd.read_csv(curr_path+'\\pts\\' + 'pt_input.csv', header=None) 
    pt_input = df.values 
    
    # cloest pt
    cloest_list=[]
    for each_p in pt_input:
        cloest_p=one_point_cloest(pt_cloud,each_p, k=1)
        cloest_list.append(cloest_p.tolist())
    cloest_pts=np.array(cloest_list)

    df=pd.DataFrame(cloest_pts)
    df.to_csv(curr_path+'\\pts\\' +'pt_output_closest.csv', index=False, header=None)
    print('end of process')