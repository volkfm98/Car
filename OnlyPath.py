import Map

#only for map testing
class Car:

    def CityRoad(self):

        self.map = Map.MyMap(open('graph.txt'))  # нам нужна карта для построения маршрута
        for dot in self.map.dots:
            if dot.id == 1:
                self.startDot = dot
            if dot.id == 18:
                self.finishDot = dot

        Path = self.map.FindTheWay(self.startDot, self.finishDot)  # теперь наш путь лежит в path
        for joint in self.map.joints:
            if joint.id==-1:
                self.prev=joint
        while (self.startDot != self.finishDot):  # пока не доехали до финиша
            for joint in Path:
                direction = self.map.GetTurnDirection(self.prev,joint)  # смотрим направление поворота на данном перекресте
                print(self.prev.id, joint.id, direction)
                self.prev = joint  # для вычисления следующего направления запоминаем ребро по которому поехали
                self.startDot = joint.GetNegative(self.startDot)
        return 2


c=Car()
c.CityRoad()