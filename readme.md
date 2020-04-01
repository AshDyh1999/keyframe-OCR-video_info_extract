# Keyframe_ocr_video
这里是使用ocr技术对视频关键帧进行光学文字识别的项目。  
主要使用帧差法判别关键帧，以及使用baidu ocr API对关键帧进行文字光学识别，同时用到图像处理的技术提高ocr识别准确性，最后对汇总的数据进行可视化处理。
## 文件目录

### keyframes_extract.py
该文件读入mp4视频文件，使用帧差法判定相邻帧的相关性从而确定关键帧，并将其提取到key_frames文件夹，同时，将时间等关键信息图片单独提取到time_info文件夹，并且将灰度处理的后的图片提取到gray_fixed_img文件夹。

### baidu_ocr_api.py
调用百度OCR接口实现对上一步提取到的图片OCR识别，并且将结果存入项目根目录下的csv文件

### show.py
读取上一步得到的csv文件，将数据动态可视化