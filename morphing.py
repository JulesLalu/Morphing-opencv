import numpy as np
import cv2
from scipy.spatial import Delaunay
from math import *
from transform import *

inpt1 = cv2.imread('C:/Users/jules/Pictures/homme.png')
inpt2 = cv2.imread('C:/Users/jules/Pictures/chat.png')
inpt1_copy = inpt1.copy()
inpt2_copy = inpt2.copy()

height_1,width_1=inpt1.shape[:2]
height_2,width_2=inpt2.shape[:2]

list_pt1=[]
list_pt2=[]

def click_event(event, x, y, flags, params):
	global counter
	if event == cv2.EVENT_LBUTTONDOWN:
		if counter%2==0:
			cv2.circle(inpt1_copy,(x,y),3,(0,0,255),thickness=-1)
			cv2.imshow('homme', inpt1_copy)
			list_pt1.append((x,y))
		else:
			cv2.circle(inpt2_copy,(x,y),3,(0,0,255),thickness=-1)
			cv2.imshow('chat', inpt2_copy)
			list_pt2.append((x,y))

for counter in range(28):
	print(counter)
	print(list_pt1)
	print(list_pt2)
	if counter%2==0:
		cv2.imshow('homme',inpt1_copy)
		cv2.setMouseCallback('homme', click_event)
		cv2.waitKey(0)
	if counter%2!=0:
		cv2.imshow('chat',inpt2_copy)
		cv2.setMouseCallback('chat', click_event)
		cv2.waitKey(0)

pt1=np.asarray(list_pt1)
pt2=np.asarray(list_pt2)

list_pt1.extend([(0.0,0.0),(0.0,float(height_1)),(float(width_1),0.0),(float(width_1),float(height_1))])
list_pt2.extend([(0.0,0.0),(0.0,float(height_1)),(float(width_1),0.0),(float(width_1),float(height_1))])

#compute Delaunay t  riangulation from 25 matches
pt1=np.asarray(list_pt1)
pt2=np.asarray(list_pt2)
tri=Delaunay(list_pt1)
simplices = tri.simplices
imgs=[]
num_frames = 25
find=find_corners(pt1)

for frame_num in range(num_frames):

	frame_num_2=num_frames-1-frame_num
	transfo_pt1=np.zeros(pt1.shape)
	transfo_pt2=np.zeros(pt2.shape)
	
	for i in range(transfo_pt1.shape[0]):
		transfo_pt1[i][0],transfo_pt1[i][1]=transform_corners(pt1[i][0],pt1[i][1],pt2[i][0],pt2[i][1],num_frames, frame_num)
		transfo_pt2[i][0],transfo_pt2[i][1]=transform_corners(pt2[i][0],pt2[i][1],pt1[i][0],pt1[i][1],num_frames, frame_num_2)

	output1 = np.zeros(inpt1.shape, dtype=inpt1.dtype)
	output2 = np.zeros(inpt1.shape, dtype=inpt1.dtype)
	for i in range(simplices.shape[0]) :
		src_1 = pt1[simplices][i]
		src_1 = np.float32(src_1.astype(int))
		transfo_1 = transfo_pt1[simplices][i]
		transfo_1 = np.float32(transfo_1.astype(int))
		src_2 = pt2[simplices][i]
		src_2 = np.float32(src_2.astype(int))
		transfo_2 = transfo_pt2[simplices][i]
		transfo_2 = np.float32(transfo_2.astype(int))
		output1=warp_tri(inpt1, src_1, transfo_1,output1)
		output2=warp_tri(inpt2, src_2, transfo_2,output2)

	output3 = cv2.addWeighted(output1, 1-(frame_num/num_frames), output2, frame_num/num_frames, 0.0)
	cv2.imshow('image no %d' % frame_num, output3)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


