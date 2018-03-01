import Map
class Car:

    def CityRoad(self):

        self.map = Map.MyMap(open('newmap.txt'))  # нам нужна карта для построения маршрута
        for dot in self.map.dots:
            if dot.id == 1:
                startDot = dot
            if dot.id == 18:
                finishDot = dot
        self.map.SetDirections(open('newdirections.txt'))

        Path = self.map.FindTheWay(startDot, finishDot)  # теперь наш путь лежит в path
        prev = str(-1)  # -2 если на втором повороте заехали, -1 если на первом для клучей
        # идея такая пытаемся поехать в нужном направлении не получилось удаляем ребро, по новой считаем
        for joint in Path:
            if joint.id==21:
                joint.Delete()
        Path = self.map.FindTheWay(startDot, finishDot)
        while (startDot != finishDot):  # пока не доехали до финиша
            for joint in Path:

                direction = self.map.directions[prev + str(joint.id)]  # смотрим направление поворота на данном перекресте
                print(prev, joint.id, direction)
                prev = str(joint.id)  # для вычисления следующего направления запоминаем ребро по которому поехали
                startDot = joint.GetNegative(startDot)
        return 2


c=Car()
c.CityRoad()