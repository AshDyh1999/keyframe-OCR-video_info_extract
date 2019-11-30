from PIL import Image
import cv2

def splitFrames(videoFileName):
    cap = cv2. VideoCapture(videoFileName) # 打开视频文件
    num = 1
    while True:
        # success 表示是否成功，data是当前帧的图像数据；.read读取一帧图像，移动到下一帧
        success, data = cap.read()
        if not success:
            break
        im = Image.fromarray(data) # 重建图像
        im.save('C:/Users/Taozi/Desktop/2019.04.30/' +str(num)+".jpg") # 保存当前帧的静态图像
        num = num + 1
        print(num)
    cap.release()
#视频路径
splitFrames('')
