import Map
import LineDetector
import CarControl
from Detector import Detector
import cv2
from threading import Thread

class Car: #три основных метода которые будут использоваться на соревнованиях MainRoad,CityRoad и Parking
    def __init__(self,device,video_source=0): #тут бы по хорошему проинициализировать все что у нас написано
        self.CarCon=CarControl(device) # кар контролу передаем девайс которым пользуемся
        self.TroubleDet=self.TroubleChecking(video_source)
        self.LineDet=self.LineChecking(video_source)

    class TroubleChecking(Thread):  #поток для детектирования знаков и ситуаций на дороге
        def __init__(self,video_source):
            Thread.__init__(self)
            self.Detector=Detector('signs/model.yaml','signs/model.h5','semafor/model.yaml','semafor/model.h5',True,video_source)
            self.crossroad=0
            self.signs = 0
            self.RedIsON=False
            self.mark=False

        def run(self): # по задумке 0-прямая дорога, 1-перекресток, 2-знак,3-препятствие
            self.mark=True
            frame = self.cap.read()[1]
            while (self.mark and self.Detector.cap.isOpened() and len(frame) > 0):
                    frame = cv2.resize(frame, self.Detector.size, interpolation=cv2.INTER_CUBIC)
                    self.signs = self.Detector.detectSigns(frame, self.Detector.printFlag)
                    self.RedIsON = self.Detector.detectSemafors(frame,self.Detector.printFlag) #1 - кирпич (красный знак стоп) 3 - движение вперед 4 - направо 5 - налево 6 - прямо или направо 7 - прямо или налево
                    frame = self.Detector.cap.read()[1]
                    self.crossroad = self.Detector.DetectCrossroads()  # так этого нет но оно бы пригодилось

            self.Detector.cap.release()


    '''Конструктить'''
    class LineChecking(Thread):  #поток для детектирования полос
        def __init__(self,video_source):
            Thread.__init__(self)
            self.cap = cv2.VideoCapture(video_source)
            self.lines = 0
            self.mark=False

        def run(self):
            self.mark=True
            frame = self.cap.read()[1]
            vecs = [[-3, -1, 70], [3, -1, 70]]
            self.Road = LineDetector.RoadControl(frame, 240, vecs, viz=True)

            while (self.mark):
                self.Detector.line_detector.img = frame
                print(self.Road.poke())
                self.lines = self.Road.poke()






    '''идеально'''
    def SemaforHandler(self):
        while (self.TroubleDet.RedIsON):
            pass
        return

    '''разобраться со знаками'''
    def SignHandler(self,sign): #метод обработки знаков
        if (sign==1):#кирпич
            pass
        elif (sign==3):#движение вперед
            pass
        elif (sign == 4):#направо
            pass
        elif (sign == 5):#налево
            pass
        elif (sign == 6):#прямо или направо
            pass
        elif (sign == 7):#прямо или налево
            pass
        else:
            pass
        return



    '''метод проезда перекрестка'''
    def TurnOn(self,direction): # поворот
        if direction==0: #едем прямо
            while (NotCrossed): #как-то задетектить что мы проехали участок
                self.CarCon.move()
                self.CarCon.turn()
        if direction==1: #поворот вправо
            while (NotCrossed): #как-то задетектить что мы проехали участок
                self.CarCon.move()
                self.CarCon.turn()
        if direction==-1: #поворот влево
            while (NotCrossed): #как-то задетектить что мы проехали участок
                self.CarCon.move()
                self.CarCon.turn()
        if direction==2: #выезд на круговое
            while (NotCrossed): #как-то задетектить что мы проехали участок
                self.CarCon.move()
                self.CarCon.turn()
        if direction==-2: #разворот
            while (NotCrossed): #как-то задетектить что мы проехали участок
                self.CarCon.move()
                self.CarCon.turn()
        return




    '''тут надо настроить оцентрирование'''
    def StayOnTheLine(self):
        while(self.TroubleDet.crossroad==0): #проверяем что ничего нового не встретилось
            if (self.TroubleDet.signs!=0):
                self.SignHandler(self.TroubleDet.signs)
            else:
                if self.LineDet.lines==2: #надо поменять
                    pass
                    #отворачиваем
                if self.LineDet.lines == 1:  # надо поменять
                    pass
                    #отворачиваем
                else:
                    self.CarCon.move() #прямо

        return self.TroubleDet.crossroad #иначе завершаем движение и выдаем почему завершили

    '''тут надо павла просить'''
    def LookAround(self):  #детект парковки



        return


    '''почти все отлично но перекрестки!!'''
    def MainRoad(self):# просто едем по по линии и поворачиваем на первых? поворотах направо
        self.TroubleDet.start()
        self.LineDet.start()
        for i in range(2):#всего два поворота ведь так7
            self.StayOnTheLine(); #держимся нашей прямой
            if (self.TroubleDet.signs==6 or self.TroubleDet.crossroad==1 or self.TroubleDet.signs==4): #поворот открылся направо
                # на самом деле достаточно знать только что правый поворот открыт но пока можно говорить что это все перекрестки
                self.TurnOn(1)
        self.TroubleDet.mark = False
        self.LineDet.mark = False
        return 1  # по идее должна вернуть значение обозначающее на каком повороте мы заехали


    '''детектор знаков сюда встроить'''
    def CityRoad(self):
        self.TroubleDet.start()
        self.LineDet.start()
        self.map = Map.MyMap(open('newmap.txt')) #нам нужна карта для построения маршрута
        for dot in self.map.dots:
            if dot.id==1:
                startDot=dot
            if dot.id==18:
                finishDot=dot
        self.map.SetDirections(open('newdirections.txt'))
        Path=self.map.FindTheWay(startDot,finishDot) #теперь наш путь лежит в path
        prev=str(-2) #-2 если на втором повороте заехали, -1 если на первом для клучей
        #идея такая пытаемся поехать в нужном направлении не получилось удаляем ребро, по новой считаем
        while (startDot!=finishDot): #пока не доехали до финиша
            for joint in Path:
                direction=self.map.directions[prev+str(joint.id)] #смотрим направление поворота на данном перекресте
                self.Car.TurnOn(direction) #поворачиваем на повороте 0 прямо 1 право -1 влево 2 круговое движение
                trouble=self.StayOnTheLine() #едем и держимся линии пока ничего не мешает
                prev=str(joint.id) #для вычисления следующего направления запоминаем ребро по которому поехали
                if (self.TroubleDet.signs!=1): #если что-то помешало придется вернутся и перестроить маршрут удаляя это ребро
                    #аналогично if(trouble==3) можно использовать
                    joint.Delete()
                    Path=self.map.FindTheWay(startDot,finishDot)
                    self.TurnOn(-2) #придется развернутся -2 разворот
                    break
            else:
                startDot=joint.GetNegative(startDot)#если оказались на перекрестке продолжаем движение'''

        self.TroubleDet.mark = False
        self.LineDet.mark = False
        return 2


    '''ага'''
    def CircleRoad(self):








        return 3



    '''тут все доделать'''
    def Parking(self):
        self.TroubleDet.start()
        self.LineDet.start()
        self.LookAround()#надо как-то осмотреться
        self.TroubleDet.mark = False
        self.LineDet.mark = False
        return 4





