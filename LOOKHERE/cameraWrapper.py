# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 00:47:51 2018

@author: Илья
"""
import cv2
import time

from picamera.array import PiRGBArray
from picamera import PiCamera

import CarSettings as CarSettings
from objectDetector import objectDetector

#инициализируем камеру
camera = PiCamera()
camera.resolution = (CarSettings.PiCameraResW,CarSettings.PiCameraResH)
camera.framerate = CarSettings.PiCameraFrameRate
camera.vflip = True
camera.hflip = True
rawCapture = PiRGBArray(camera, size=(CarSettings.PiCameraResW,CarSettings.PiCameraResH))

time.sleep(0.1)

#создаем объект распознавателя знаков
dtc = objectDetector()

#цикл получения кадра из камеры
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    image = frame.array
    
    #оригинальный фрейм
    cv2.imshow('original frame', frame)
    
    #данные от детекторов знаков и светофоров подряд
    isBrick = dtc.DetectRedSign(image,True)
    BSign = dtc.DetectBlueSign(image,True)
    isTrLight = dtc.DetectTrLight(frame,True)
    
    #дебаг-вывод
    print('----')
    print('isRedBrick:{}'.format(isBrick))
    print('isBlueSign:{}'.format(BSign))
    print('isBlueSign:{}'.format(isTrLight))
    
    #обработанный фрейм
    cv2.imshow('processed frame', frame)
    
    k=cv2.waitKey(30) & 0xff
    if k == 27:
        break;
    
    #очистка кадра. важная штука!
    rawCapture.truncate(0)

cv2.destroyAllWindows()