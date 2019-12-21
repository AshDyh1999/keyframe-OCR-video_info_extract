import base64
from urllib import parse, request
import json
import os
import csv
from PIL import Image
import cv2

#zbw
# ak = 'VV5rAjwWQZHLonbN0DXtg4jN'
# sk = 'lPE8VqkbkT2T3opkt1XvPGxZRcytIiM5'

#mine
# ak = 'v4ri9rThSC29iKyPufgCDUTa'
# sk = 'al9FONUC6aEynghjpODQXLGyCgibTeKD'

#zjt
ak = '4y4H1UDLKgUIm2O0hX0MtTP7'
sk = '0WxOr29QcyGDHI51Q8YA3q5VM78dYxfB'
def GetAccessToken(ak, sk):
    '''
    获取access_token代码
    :param ak:控制台应用API Key
    :param sk:控制台应用Secret Key
    :return:返回接口调用的access_token参数以及token的有效期（单位为秒）
    '''

    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (
        ak, sk)
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    req = request.Request(method='GET', url=host, headers=headers)
    response = request.urlopen(req)
    if (response.status == 200):
        data = json.loads(response.read().decode())
        access_token = data['access_token']
        expires_in = data['expires_in']
        return access_token, expires_in

def RecogniseGeneral(access_token, apitype='accurate_basic',image=None, url=None, recognize_granularity='big', language_type='CHN_ENG',
                     detect_direction=False, detect_language=False, vertexes_location=False, probability=False):
    '''
    通用文字识别（含位置信息）
    :param access_token:URL参数，需要拼接到接口URL上
    :param image:图像数据，base64编码，要求base64编码后大小不超过4M，最短边至少15px，最长边最大4096px,支持jpg/png/bmp格式，当image字段存在时url字段失效
    :param url:图片完整URL，URL长度不超过1024字节，URL对应的图片base64编码后大小不超过4M，最短边至少15px，最长边最大4096px,支持jpg/png/bmp格式，当image字段存在时url字段失效，不支持https的图片链接
    :param recognize_granularity:是否定位单字符位置，big：不定位单字符位置，默认值；small：定位单字符位置
    :param language_type:识别语言类型，默认为CHN_ENG。可选值包括：- CHN_ENG：中英文混合；- ENG：英文；- POR：葡萄牙语；- FRE：法语；- GER：德语；- ITA：意大利语；- SPA：西班牙语；- RUS：俄语；- JAP：日语；- KOR：韩语
    :param detect_direction:是否检测图像朝向，默认不检测，即：false。朝向是指输入图像是正常方向、逆时针旋转90/180/270度。可选值包括:- true：检测朝向；- false：不检测朝向。
    :param detect_language:是否检测语言，默认不检测。当前支持（中文、英语、日语、韩语）
    :param vertexes_location:是否返回文字外接多边形顶点位置，不支持单字位置。默认为false
    :param probability:是否返回识别结果中每一行的置信度
    :return:https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic
    '''
    host = 'https://aip.baidubce.com/rest/2.0/ocr/v1/%s?access_token=%s' % (apitype,access_token)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    formdata = {'recognize_granularity': recognize_granularity, 'language_type': language_type,
                'detect_direction': detect_direction, 'detect_language': detect_language,
                'vertexes_location': vertexes_location, 'probability': probability}
    if image is not None:
        formdata['image'] = image
    elif url is not None:
        formdata['url'] = url
    data = parse.urlencode(formdata).encode('utf8')
    req = request.Request(method='POST', url=host, headers=headers, data=data)
    response = request.urlopen(req)
    # print(response)
    if (response.status == 200):
        jobj = json.loads(response.read().decode())
        response.close()
        datas = jobj['words_result']
        recognise = []
        for obj in datas:
            recognise.append(obj["words"])
        
        return recognise
        
def Recognise(img_name):
    access_token, expires_in = GetAccessToken(ak, sk) # 将此ak与sk替换成自己应用的值
    
    time_img_path = './time_info/'
    fixed_img_path = './fixed_img/'
    gray_fixed_img_path = './gray_fixed_img/'
    
    with open(file=time_img_path + img_name, mode='rb') as file:
        base64_data = base64.b64encode(file.read())
        recognise_time = RecogniseGeneral(apitype='accurate_basic',access_token=access_token, image=base64_data)
   
    with open(file=fixed_img_path + img_name, mode='rb') as file:
        base64_data = base64.b64encode(file.read())
        recognise_fix = RecogniseGeneral(apitype='webimage',access_token=access_token, image=base64_data)
   
    with open(file=gray_fixed_img_path + img_name, mode='rb') as file:
        base64_data = base64.b64encode(file.read())
        gray_recognise_fix = RecogniseGeneral(apitype='webimage',access_token=access_token, image=base64_data)

    #剔除不必要的数据，如开始的度量值，以及中间出现的Popular Programming Languages
    result = []
    if len(recognise_fix) > len(gray_recognise_fix):
        recognise = recognise_fix
    else:
        recognise = gray_recognise_fix

    flag=0
    for i in recognise:
        if i[0] >= 'A' and i[0] <= 'Z':
            flag=1
        if i =='Popular' or i=='Programming' or i=='Languages':
            continue
        if flag==1:
            result.append(i)

    if len(result):
        #将最后一项时间提到列表刚开始,表示为1999.Q1
        year=recognise_time[0][:4]
        quarter=recognise_time[0][-2:]
        time=year+"."+quarter
        result.insert(0,time)
        return result
    else:
        return result

def Recognise_test(img_path):
    access_token, expires_in = GetAccessToken(ak, sk) # 将此ak与sk替换成自己应用的值
    with open(file=img_path, mode='rb') as file:
        base64_data = base64.b64encode(file.read())
    # 调用iOCR自定义模板文字识别接口
    # recognise = RecogniseForm(access_token=access_token, image=base64_data,templateSign=templateSign)    # 将此templateSign替换成自己设置的模板值
    recognise = RecogniseGeneral(apitype='webimage' ,access_token=access_token, image=base64_data) #general_basic accurate_basic
    result = []
    flag=0
    for i in recognise:
        if i[0] >= 'A' and i[0] <= 'Z':
            flag=1
        if i =='Popular' or i=='Programming' or i=='Languages':
            continue
        if flag==1:
            result.append(i)
    return result

if __name__ == '__main__':

    fixed_img_path = './fixed_img'
    # fixed_img_path = './key_frames'
    # all_fixed_imgs = os.listdir(fixed_img_path)

    # all_fixed_imgs.sort(key=lambda x: int(x.split('.')[0]))  # 排序
    # premsg=['']
    # for img in all_fixed_imgs:
    #     print("处理%s中......" % img)
    #     img1 = cv2.imread(fixed_img_path+'/'+img, -1)
    #     msg = Recognise(img)
    
    #     #结尾几张图片一致就相当于结束了
    #     if msg[0]==premsg[0]:
    #         break
    #     #写入csv
    #     with open('test2.csv', 'a+', newline='')as f:
    #         f_csv = csv.writer(f)
    #         f_csv.writerow(msg)
    #     #记录上一组值
    #     premsg=[]
    #     for i in msg:
    #         premsg.append(i)


    # 测试单个图片用186 187 193-197 202-208---------------------------85原图优秀212灰度优秀
    number = '212'
    img_path = fixed_img_path + '/' + number + '.jpg'
    img = cv2.imread(img_path, -1)
    height, width = img.shape[:2]
    # 放大图像
    fx = 2
    fy = 2
    enlarge = cv2.resize(img, (0, 0), fx=fx, fy=fy, interpolation=cv2.INTER_CUBIC)

    cv2.imwrite(number + '_large.png', enlarge)

    img2 = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imwrite(number + '_gray.png', img2)
    
    #原图像
    msg = Recognise_test(img_path)
    print('图像路径:'+img_path)
    print('原始图像：%s' %msg)
    #放大的图像
    msg = Recognise_test(number + '_large.png')
    print('放大图像：%s' %msg)
    #灰度图
    msg = Recognise_test(number + '_gray.png')
    print('灰度图像：%s' %msg)

    img=Image.open(fixed_img_path + '/' + number + '.jpg')
    img=img.convert('L')
    threshold=200
    table=[]
    for i in range(256):
        if i<threshold:
            table.append(0)
        else:
            table.append(1)
    imggray=img.point(table,'1')
    imggray.save(number +'_blackwhite.jpg')
    #二值图像
    msg = Recognise_test(number +'_blackwhite.jpg')
    print('二值图像：%s' %msg)

    #右部
    img_right = img[50:,140:,:]
    cv2.imwrite(number + '_right.png', img_right)
    msg = Recognise_test(number + '_right.png')
    print('右部：' + str(msg))
    #左部
    img_left = img[50:,0:140,:]
    cv2.imwrite(number + '_left.png', img_left)
    msg = Recognise_test(number + '_left.png')
    print('左部：' + str(msg))