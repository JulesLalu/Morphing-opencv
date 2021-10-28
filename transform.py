import numpy as np
from math import *
from numpy import linalg as LA
from scipy.spatial.transform import Rotation as R
from quaternionop import quaternion_multiply, quaternion_divide
import cv2
'''
def slerp(quat1, quat2, alpha):
    
    q_r=quaternion_divide(quat2,quat1)
    w_r=q_r[3]
    q_r= np.asarray(q_r)
    if w_r<0 : 
        q_r= - q_r

    v_r=q_r[0:3]

    theta_r = 2*atan(LA.norm(v_r)/w_r)

    n_r = v_r/LA.norm(v_r)

    theta_alpha = alpha * theta_r

    theta_n_r = sin(theta_alpha/2)*n_r
    q_alpha =  [theta_n_r[0], theta_n_r[1], theta_n_r[2], cos(theta_alpha/2)]

    slerp1 = quaternion_multiply(q_alpha,quat1)

    return slerp1

def rotation(R_1,R_2,num_frames, frame_num):
    r1=R.from_dcm(R_1)
    q1=r1.as_quat()
    r2=R.from_dcm(R_2)
    q2=r2.as_quat()
    q_i=slerp(q1,q2,frame_num/num_frames)
    r = R.from_quat(q_i)
    R_i=r.as_dcm()
    return R_i

def translation(t_1,t_2,num_frames, frame_num):
    t=(t_2-t_1)*frame_num/num_frames+t_1
    return t

def intrinsic(f1,f2,num_frames, frame_num,c_x_2,c_y_2):
    f_nor=(f2-f1)*frame_num/num_frames+f1
    f_inv=(f1-f2)*(num_frames-frame_num-1)/num_frames+f2
    K2_nor = np.asarray([[f_nor,0,c_x_2],[0,f_nor,c_y_2],[0,0,1]])
    K2_inv = np.asarray([[f_inv,0,c_x_2],[0,f_inv,c_y_2],[0,0,1]])
    return K2_nor,K2_inv

def transform_normal(R_1,R_incr,t_1,t_incr,x,y,K1,K2):
    R_t_init_1=np.identity(4)
    R_t_init_1[0:3,0:3]=R_1
    R_t_init_1[0:3,3]=t_1
    K_ext_1=np.identity(4)
    K_ext_1[0:3,0:3]=K1
    P_1= K_ext_1@R_t_init_1

    R_t_init_2=np.identity(4)
    R_t_init_2[0:3,0:3]=R_incr
    R_t_init_2[0:3,3]=t_incr
    K_ext_2=np.identity(4)
    K_ext_2[0:3,0:3]=K2
    P_2= K_ext_2@R_t_init_2

    M=P_2@np.linalg.inv(P_1)
    x1=np.asarray([x,y,1,0]) #we consider that the depth d = 0
    x2=M@x1
    return x2[0], x2[1]
'''
def transform_corners(x1,y1,x2,y2,num_frames, frame_num):
    x=(x2-x1)*frame_num/num_frames+x1
    y=(y2-y1)*frame_num/num_frames+y1
    return x,y

def find_corners(array):
    idx_max_x=0
    idx_max_y=0
    idx_min_x=0
    idx_min_y=0
    max_x=array[0][0]
    max_y=array[0][1]
    min_x=array[0][0]
    min_y=array[0][1]
    for i in range (array.shape[0]):
        if array[i][0]>max_x:
            idx_max_x=i
            max_x=array[i][0]
        if array[i][1]>max_y:
            idx_max_y=i
            max_y=array[i][1]
        if array[i][0]<min_x:
            idx_min_x=i
            min_x=array[i][0]
        if array[i][1]<min_y:
            idx_min_y=i
            min_y=array[i][1]
    return [idx_max_x,idx_max_y,idx_min_x,idx_min_y]
    
def warp_tri(inpt, tri1, tri2,output):
    height_1,width_1=inpt.shape[:2]
    
    r1 = cv2.boundingRect(tri1)
    r2 = cv2.boundingRect(tri2)

    tri1Cropped=[]
    tri2Cropped=[]
    for i in range(0, 3):
        tri1Cropped.append(((tri1[i][0] - r1[0]),(tri1[i][1] - r1[1])))
        tri2Cropped.append(((tri2[i][0] - r2[0]),(tri2[i][1] - r2[1])))
    
    img1Cropped = inpt[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
    warpMat = cv2.getAffineTransform(np.float32(tri1Cropped), np.float32(tri2Cropped))
    img2Cropped = cv2.warpAffine( img1Cropped, warpMat, (r2[2], r2[3]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101 )

    mask = np.zeros((r2[3], r2[2], 3), dtype = np.float32)
    cv2.fillConvexPoly(mask, np.int32(tri2Cropped), (1.0, 1.0, 1.0), 16, 0)
    img2Cropped = img2Cropped * mask
    for j in range(r2[1],r2[1]+r2[3]):
        for i in range(r2[0],r2[0]+r2[2]):
            if 0<i <width_1:
                if 0<j<height_1:
                    if mask[j-r2[1],i-r2[0]][0]==1.0 and mask[j-r2[1],i-r2[0]][1]==1.0 and mask[j-r2[1],i-r2[0]][2]==1.0 :
                        output[j, i] = img2Cropped[j-r2[1],i-r2[0]]
    return output



    

