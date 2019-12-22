import cv2
import numpy as np
import sys
from scipy.stats.stats import  pearsonr
import time
from tqdm import tqdm,trange

if __name__ == "__main__":   
    #相关性阈值
    THREADHOLD = 0.99
    #视频路径（相对路径)
    videopath = 'Most_Popular_Programming_Languages_1965_-_2019.mp4'
    #存帧的路径
    dir = './key_frames/'
    time_img_dir = './time_info/'
    fixed_img_dir = './fixed_img/'
    gray_fixed_img_dir = './gray_fixed_img/'

    #加载视频
    cap = cv2.VideoCapture(str(videopath))
    #总帧数
    frames_num=cap.get(7) 
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
    #计数读取的帧数
    i = 1 
    #计数要保存的帧数
    num = 1
    #不用while(success):换用tqdm可以展示进度条
    for i in trange(int(frames_num)-1):
        frame_time = frame[560:,800:,:]
        luv = cv2.cvtColor(frame_time, cv2.COLOR_BGR2LUV)
        curr_frame = luv
        if curr_frame is not None and prev_frame is not None:
            # 将矩阵转换成向量。按行转换成向量，第一个参数就是矩阵元素的个数
            img0= curr_frame.reshape(curr_frame.size, order='C')  
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