#-*- coding: utf-8 -*-
# import 进openCV的库
import cv2
import requests
import os
import json

###调用电脑摄像头检测人脸并截图
API_KEY = "-sCVna-uZ9e0KD-T9gZVZSnVF5n64FNt"
API_SECRET = "Mj33nqlO9f02X8WGzaGV8oEvZZ6etug7"
BASE_URL = 'http://apicn.faceplusplus.com/v2'

 



def CatchPICFromVideo(window_name, camera_idx, catch_pic_num, path_name):
    cv2.namedWindow(window_name)

    #视频来源，可以来自一段已存好的视频，也可以直接来自USB摄像头
    cap = cv2.VideoCapture(camera_idx)


    #告诉OpenCV使用人脸识别分类器
    classfier = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')

    #识别出人脸后要画的边框的颜色，RGB格式, color是一个不可增删的数组
    color = (0, 255, 0)

    num = 0
    while cap.isOpened():
        ok, frame = cap.read() #读取一帧数据
        if not ok:
            break

        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  #将当前桢图像转换成灰度图像

        #人脸检测，1.2和2分别为图片缩放比例和需要检测的有效点数
        faceRects = classfier.detectMultiScale(grey, scaleFactor = 1.2, minNeighbors = 3, minSize = (32, 32))
        if len(faceRects) > 0:          #大于0则检测到人脸
            for faceRect in faceRects:  #单独框出每一张人脸
                x, y, w, h = faceRect

                #将当前帧保存为图片
                img_name = "%s/%d.jpg" % (path_name, num)
                #print(img_name)
                image = frame[y - 10: y + h + 10, x - 10: x + w + 10]
                cv2.imwrite(img_name, image,[int(cv2.IMWRITE_PNG_COMPRESSION), 9])

                num += 1
                if num > (catch_pic_num):   #如果超过指定最大保存数量退出循环
                    break

                #画出矩形框
                cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 2)

                #显示当前捕捉到了多少人脸图片了，这样站在那里被拍摄时心里有个数，不用两眼一抹黑傻等着
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame,'num:%d/100' % (num),(x + 30, y + 30), font, 1, (255,0,255),4)

                #超过指定最大保存数量结束程序
        if num > (catch_pic_num): break

        #显示图像
        cv2.imshow(window_name, frame)
        c = cv2.waitKey(10)
        if c & 0xFF == ord('q'):
            break

            #释放摄像头并销毁所有窗口
    cap.release()
    cv2.destroyAllWindows()
    
def searchFace():
    url = 'https://api-cn.faceplusplus.com/facepp/v3/search'
    payload = {'api_key': API_KEY,
           'api_secret': API_SECRET,
           'faceset_token':'569afdf98471b26bd0ef54d321907101',
               }
    files = {'image_file':open('3.jpg', 'rb')}
    r = requests.post(url,files=files,data=payload)
    data=json.loads(r.text)
    print r.text
    if data["results"][0]["face_token"] == facetoken and data["results"][0]["confidence"]>=data["thresholds"]["1e-5"]:
        print('\nmaxlin1')
    elif data["results"][0]["face_token"] == "c116a106c02f6ffd8606408fe2fb5def"and data["results"][0]["confidence"]>=data["thresholds"]["1e-5"]:
        print('\n东maxlin2')
    else:
        print ('\n不是我们宿舍的成员')
    
    
def addCreateFacetoSet():
    url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/create'
    payload = {'api_key': API_KEY,
               'api_secret': API_SECRET,
               'display_name':'maxlin',
               'outer_id':'deerfiled',
               'face_tokens':facetoken,
               'force_merge':1
               }
    r = requests.post(url,data=payload)
    print(r.text)
    
def analyzeFace():
    url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    files = {'image_file':open('2.jpg', 'rb')}
    payload = {'api_key': API_KEY,
               'api_secret': API_SECRET,
               'return_landmark': 0,
               'return_attributes':'gender,age,glass'}
     
    r = requests.post(url,files=files,data=payload)
    data=json.loads(r.text)
    print (r.text)
    width = data['faces'][0]['face_rectangle']['width']
    top = data['faces'][0]['face_rectangle']['top']
    height = data['faces'][0]['face_rectangle']['height']
    left = data['faces'][0]['face_rectangle']['left']
    facetoken=data['faces'][0]['face_token']
    print(facetoken)
    img = cv2.imread("2.jpg")
    vis = img.copy()
    cv2.rectangle(vis, (left, top), (left+width, top+height),(0, 255, 0), 2)
    cv2.imshow("Image", vis)
    
    
if __name__ == '__main__':
    # 连续截100张图像，存进image文件夹中
    CatchPICFromVideo("get face", 0, 5, "./img")
    print("Five pics haven been taken and sending it to Owner")
    
 
 
    
     
    
    
    

