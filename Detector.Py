import cv2
import numpy as np
from numpy.linalg import norm
from Keras.models import model_from_yaml


class Detector:
    # ranges for semafors
    red_low_range_low_h = 0
    red_low_range_low_s = 100
    red_low_range_low_v = 100
    red_low_range_high_h = 5
    red_low_range_high_s = 255
    red_low_range_high_v = 255
    red_high_range_low_h = 170
    red_high_range_low_s = 100
    red_high_range_low_v = 100
    red_high_range_high_h = 179
    red_high_range_high_s = 255
    red_high_range_high_v = 255

    def __init__(self, model_signs, weights_signs, model_semafors, weights_semafors, printFlag, video_source=0,
                 resize=(640, 480)):
        # load model for signs
        yaml_file = open(model_signs, 'r')
        loaded_model_yaml = yaml_file.read()
        yaml_file.close()
        self.model_signs = model_from_yaml(loaded_model_yaml)
        self.model_signs.load_weights(weights_signs)

        # load model for semafors
        yaml_file = open(model_semafors, 'r')
        loaded_model_yaml = yaml_file.read()
        yaml_file.close()
        self.model_sem = model_from_yaml(loaded_model_yaml)
        self.model_sem.load_weights(weights_semafors)

        self.cap = cv2.VideoCapture(video_source)
        self.size = resize
        self.printFlag = printFlag  # Flag for additional drawing

    def detectSemafors(self, frame, printFlag):
        # noramalization
        frame2 = cv2.medianBlur(frame, 3)
        frame2 = cv2.GaussianBlur(frame2, (3, 3), 2)  # important for finding circles!
        # masking
        hsv_image_1 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
        red_mask_low = cv2.inRange(hsv_image_1, np.array(
            (self.red_low_range_low_h, self.red_low_range_low_s, self.red_low_range_low_v)
            , dtype="uint8"), np.array((self.red_low_range_high_h, self.red_low_range_high_s,
                                        self.red_low_range_high_v), dtype="uint8"))
        red_mask_high = cv2.inRange(hsv_image_1, np.array(
            (self.red_high_range_low_h, self.red_high_range_low_s, self.red_high_range_low_v),
            dtype="uint8"), np.array((self.red_high_range_high_h, self.red_high_range_high_s,
                                      self.red_high_range_high_v), dtype="uint8"))
        mask = cv2.addWeighted(red_mask_low, 1.0, red_mask_high, 1.0, 0.0)
        pred = False
        # additional drawing
        if (printFlag):
            cv2.imshow('Mask_Semafors', mask)
        # find a circles from mask
        cont = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[1]
        for cnt in cont:
            moments = cv2.moments(cnt, 255)
            dM01 = moments['m01']
            dM10 = moments['m10']
            dArea = moments['m00']
            if dArea > 30:  # Отбрасывание контуров по площади
                x = int(dM10 / dArea)  # x координата центра масс контура
                y = int(dM01 / dArea)  # у координата цента масс контура
                # L,R,T,B - кайние точки контура, левая, правая, верхняя, нижняя соответственно
                L = tuple(cnt[cnt[:, :, 0].argmin()][0])
                R = tuple(cnt[cnt[:, :, 0].argmax()][0])
                T = tuple(cnt[cnt[:, :, 1].argmin()][0])
                B = tuple(cnt[cnt[:, :, 1].argmax()][0])
                diam1 = R[0] - L[0]
                diam2 = B[1] - T[1]
                r = int((diam1 + diam2) / 4)  # средний радиус контура
                if (
                        y > 3 * r and x > 3 * r and diam1 / diam2 > 0.85 and diam1 / diam2 < 1.15):  # первые 2 условия для корректного вырезания контура
                    cut_frame = []
                    if r < 5:  # С этими условиями результат получается лучше
                        cut_frame = frame[(y - r * 3):(y + r * 9), (x - r * 3):(x + r * 3)]
                    else:
                        cut_frame = frame[(y - r * 2):(y + r * 7), (x - r * 2):(x + r * 2)]
                    cut_frame = cv2.resize(cut_frame, (16, 48), interpolation=cv2.INTER_CUBIC)
                    k = self.model_sem.predict(np.expand_dims(np.array(cut_frame.astype("float") / 255.0), axis=0))
                    # print(k)
                    if k > 0.8:
                        pred = True
                        if (printFlag):
                            frame = cv2.rectangle(frame, (x - r * 3, y - r * 3), (x + r * 3, y + r * 8), (0, 0, 255), 2)
        return pred

    def detectSigns(self, frame, printFlag):
        # noramalization
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
        frame2 = cv2.medianBlur(frame, 3)
        frame2 = cv2.GaussianBlur(frame2, (3, 3), 2)  # important for finding circles!
        # masking
        hsv_image_1 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
        low_blue = (105, 120, 50)
        hight_blue = (120, 255, 255)
        mask = cv2.inRange(hsv_image_1, low_blue, hight_blue)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        if (printFlag):
            cv2.imshow('Mask_Signs', mask)
        circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 0.7, minDist=50, param1=70, param2=10, minRadius=15,
                                   maxRadius=40)  # let's change params
        pred = []
        if np.all(circles) != None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                if ((x - r) > 0 and (x + r) > 0 and (y - r) > 0 and (y + r) > 0):
                    cut_frame = frame2[y - r:y + r, x - r:x + r]
                    cut_frame = cv2.resize(cut_frame, (32, 32), interpolation=cv2.INTER_CUBIC)
                    k = self.model_signs.predict(np.expand_dims(np.array(cut_frame.astype("float") / 255.0), axis=0))
                    maximum = max(k[0])
                    index = np.where(k[0] == maximum)[0][0]
                    # print(str(maximum)+" "+str(index))
                    if (maximum > 0.5):
                        print(str(maximum) + " " + str(index))
                        pred.append(index)
                        if (printFlag):
                            frame = cv2.rectangle(frame, (x - r, y - r), (x + r, y + r), (0, 0, 255), 2)
                            cv2.imshow('Sign_cut:' + str(index), cut_frame)
        return pred
