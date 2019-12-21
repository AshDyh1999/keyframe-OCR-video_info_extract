import cv2
import operator
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.signal import argrelextrema
from scipy.stats.stats import  pearsonr
import time
from tqdm import tqdm,trange

if __name__ == "__main__":
    print(sys.executable)
    THREADHOLD = 0.99
    #Video path of the source file
    videopath = 'Most_Popular_Programming_Languages_1965_-_2019.mp4'
    #Directory to store the processed frames
    dir = './key_frames/'
    time_img_dir = './time_info/'
    fixed_img_dir = './fixed_img/'
    gray_fixed_img_dir = './gray_fixed_img/'
    print("target video :" + videopath)
    print("key_frames save directory: " + dir)

    # load video and compute diff between frames
    cap = cv2.VideoCapture(str(videopath)) 
    curr_frame = None
    prev_frame = None 
    frame_coor = []
    frames = []
    #开始计时
    start_time = time.time()
    
    #单独保存第一帧
    success, frame = cap.read()
    cv2.imwrite(dir + "1.jpg", frame)
    frame_time = frame[560:,800:,:]
    cv2.imwrite(time_img_dir + "1.jpg", frame_time)
    frame_fixed = frame
    frame_fixed[300:,810:,:] = 255
    cv2.imwrite(fixed_img_dir + "1.jpg", frame_fixed)
    frame_fixed_gray = cv2.cvtColor(frame_fixed, cv2.COLOR_RGB2GRAY)
    cv2.imwrite(gray_fixed_img_dir + '1.jpg', frame_fixed_gray)
    
    i = 1 
    num = 1
    # while(success):
    for i in trange(8903):
        frame_time = frame[560:,800:,:]
        luv = cv2.cvtColor(frame_time, cv2.COLOR_BGR2LUV)
        curr_frame = luv
        if curr_frame is not None and prev_frame is not None:
            #logic here
            img0= curr_frame.reshape(curr_frame.size, order='C')  # 将矩阵转换成向量。按行转换成向量，第一个参数就是矩阵元素的个数
            img1= prev_frame.reshape(prev_frame.size, order='C')
            # corr = np.corrcoef(img0, img0)[0, 1]
            #皮尔逊相关系数0.99为阈值
            corr = pearsonr(img0,img1)[0]
            if corr <= THREADHOLD:
                num += 1
                # print(i)
                #rgb = cv2.cvtColor(frame, cv2.COLOR_LUV2BGR)
                name = str(num) + ".jpg"
                cv2.imwrite(dir + name, frame)
                cv2.imwrite(time_img_dir + name ,frame_time)
                frame_fixed = frame
                frame_fixed[300:,810:,:] = 255
                cv2.imwrite(fixed_img_dir + name, frame_fixed)
                frame_fixed_gray = cv2.cvtColor(frame_fixed, cv2.COLOR_RGB2GRAY)
                cv2.imwrite(gray_fixed_img_dir + name, frame_fixed_gray)
        prev_frame = curr_frame
        i = i + 1
        success, frame = cap.read()   
    cap.release()
    end_time = time.time()
    print("耗时：",end_time - start_time,'s')