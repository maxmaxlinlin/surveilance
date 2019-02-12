#-*- coding: utf-8 -*-
# import 进openCV的库
import cv2
import requests
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import encoders
    
    
    
###调用电脑摄像头检测人脸并截图
API_KEY = "-sCVna-uZ9e0KD-T9gZVZSnVF5n64FNt"
API_SECRET = "Mj33nqlO9f02X8WGzaGV8oEvZZ6etug7-1"
BASE_URL = 'http://apicn.faceplusplus.com/v2'
UserName='maxmaxlamlam@gmail.com'
UserPassword='you  need to turn on the less secure app setting in your google account which is not recommended by google'
Server=smtplib.SMTP('smtp.gmail.com:587')

def SendMail(ImgFileName):
    fromaddr = "maxmaxlamlam@gmail.com"
    toaddr = "maxmaxlamlam@gmail.com"
    msg = MIMEMultipart()
     
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "SUBJECT OF THE EMAIL"
     
    body = "TEXT YOU WANT TO SEND"
     
    msg.attach(MIMEText(body, 'plain'))
     
    filename = ImgFileName
    attachment = open(ImgFileName, "rb")
     
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
     
    msg.attach(part)
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "benbenQq3344")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()






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
                cv2.putText(frame,'num:%d/5' % (num),(x + 30, y + 30), font, 1, (255,0,255),4)

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
    
    
def searchFace(facesetToken,faceToken,adminToken,pic):
    print("---------------------------")
    print("In search facesetToken is "+facesetToken)
    print("In search faceToken is "+faceToken)
    print("In search adminToken is "+adminToken)
    print("In search pic is "+pic)

    url = 'https://api-cn.faceplusplus.com/facepp/v3/search'
    payload = {'api_key': API_KEY,
           'api_secret': API_SECRET,
           'faceset_token':facesetToken,
               }
    files = {'image_file':open(pic, 'rb')}
    r = requests.post(url,files=files,data=payload)
    data=json.loads(r.text)
    print (r.text)
    if data["results"][0]["face_token"] == adminToken and data["results"][0]["confidence"]>=data["thresholds"]["1e-5"]:
        print('\n -----------------------------------You are admin--------------------')
    elif data["results"][0]["face_token"] == faceToken and data["results"][0]["confidence"]>=data["thresholds"]["1e-5"]:
        print('\n ----------------------------------Hello Members---------------------')
    else:
        print ('\n---------------------------------you dont belongs here--ALIENS!-------sending alerts to master---------')
        SendMail('/home/pi/Desktop/monitoring/0.jpg')
    


def addCreateFacetoSet(facetoken):
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
    data=json.loads(r.text)
    faceSettoken=data['faceset_token']
    print("faceSettoken is "+faceSettoken)
    return faceSettoken

def analyzeFace(face):
    url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    files = {'image_file':open(face, 'rb')}
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
   # print(facetoken)
    img = cv2.imread("./admin/2.jpg")
    vis = img.copy()
    cv2.rectangle(vis, (left, top), (left+width, top+height),(0, 255, 0), 2)
    cv2.imshow("Image", vis)
    print("face token is "+facetoken)
    return facetoken
    
    
if __name__ == '__main__':
    # 连续截10张图像，存进admin文件夹中
    print("You are at admin mode now: Taking five photos for the adminstrators")
    CatchPICFromVideo("get face", 0, 5, "./admin")
    print("Five pics haven been taken and now uploading administator to cloud")
    adminFace=analyzeFace('./admin/1.jpg')
    adminToken=adminFace
    facesetT=addCreateFacetoSet(adminFace)
    searchFace(facesetT,adminToken,adminToken,'./admin/1.jpg')
   
    message = input("Press 1 for minitor mode and 2 for adding new people to the system:")
    message=int(message)
    
    
    while(message):
        if message==1:
                CatchPICFromVideo("get face", 0, 5, "./monitoring")
                vistorFaceToken=analyzeFace('./monitoring/1.jpg')
                searchFace(facesetT,vistorFaceToken,adminToken,'./minitoring/1.jpg')
        elif message==2:
                print("You are Now recording new members to system, please stand still")
                CatchPICFromVideo("get face", 0, 5, "./members")
                print("Five pics of the member haven been taken and now uploading Members to cloud")
                MembersFace=analyzeFace('./members/1.jpg')
                facesetT=addCreateFacetoSet(MembersFace)
                searchFace(facesetT,MembersFace,adminToken,'./members/1.jpg')
                message=1;
                print("go back to moniroting mode")


                        
        
 
    
     
    
    
    


