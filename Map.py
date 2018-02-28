class Dot: #точки
    def __init__(self,id):
        self.id=id
        self.joinedJoints=[]
    def AddJoint(self,Joint):
        self.joinedJoints.append(Joint)
    pass
class Joint: #ребра
    def __init__(self,leftDot,rightDot,len,k):
        self.leftDot=leftDot;
        self.rightDot=rightDot;
        self.len=len;
        self.id=k
    def Delete(self):
        self.leftDot.joinedJoints.remove(self)
        self.rightDot.joinedJoints.remove(self)
    def GetNegative(self,test):
        if self.leftDot==test:
            return self.rightDot
        if self.rightDot==test:
            return self.leftDot
        return
    pass
class MyMap: #карта
    dots = []
    joints=[]
    directions={}
    def __init__(self,file): #инициализируем карту из файла
        s=file.readline().split()
        while (int(s[0])!=-1):
            left=int(s[0])
            right=int(s[1])
            dist=int(s[2])
            jointnum=int(s[3]) #номер ребра
            seenLeft=False
            seenRight=False
            for d in self.dots:
                if d.id==left:
                    seenLeft=True
                    leftDot=d
                if d.id==right:
                    seenRight=True
                    rightDot=d
            if not seenLeft :
                leftDot=Dot(left)
                self.dots.append(leftDot)
            if not seenRight:
                rightDot = Dot(right)
                self.dots.append(rightDot)
            newjoint = Joint(leftDot, rightDot, dist,jointnum)
            self.joints.append(newjoint)
            leftDot.AddJoint(newjoint)
            rightDot.AddJoint(newjoint)
            s = file.readline().split()
    def SetDirections(self,file):
        s = file.readline().split()
        while (s[0]!='-3'):
            self.directions[s[0]+s[1]]=int(s[2])
            s=file.readline().split()
    minimumScore=1000000
    minimumPath=[]
    workingStack=[]
    def WayTemp(self,startDot,finishDot,score): #рекурсивный поиск
        self.workingStack.append(startDot)
        if startDot==finishDot:
            if score<self.minimumScore:
                self.minimumScore=score
                self.minimumPath=[]
                for Dot in self.workingStack:
                    self.minimumPath.append(Dot)
            self.workingStack.pop()
            return
        for joint in startDot.joinedJoints:
            newPoint=joint.GetNegative(startDot)
            if newPoint==startDot:
                continue
            if newPoint in self.workingStack:
                continue
            newscore=score+joint.len
            self.WayTemp(newPoint,finishDot,newscore)
        self.workingStack.pop()

    def GetJoint(self, leftDot, rightDot):
        for joint in leftDot.joinedJoints:
            if joint.GetNegative(leftDot) == rightDot:
                return joint
    def FindTheWay(self,startDot,finishDot): #алгоритм поиска пути начинается тут
        self.WayTemp(startDot,finishDot,0)
        prev = 0
        path=[]
        for dot in self.minimumPath:
            if prev != 0:
                path.append(self.GetJoint(prev,dot))
            prev = dot
        self.minimumScore=1000000
        return path

    def __del__(self):
            for joint in self.joints:
                del joint
            for dot in self.dots:
                del dot


