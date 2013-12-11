import random

class IData(object):
    instanceName = ""
    daysNum = 0
    periodsPerDay = 0

    def __str__(self):
        return " ".join([self.instanceName, (self.daysNum), str(self.periodsPerDay)])

class Data(IData):
    """Old data structure, linear search time for objects by ids"""
    def __init__(self):
        self.courses = []
        self.rooms = []
        self.curricula = []
        self.constraints = []

        self.instanceName = ""
        self.daysNum = 0
        self.periodsPerDay = 0

    def __str__(self):
        return " ".join([str(self.daysNum), str(self.periodsPerDay)])




    def getAllCourses(self):
        return self.courses

    def getAllRooms(self):
        return self.rooms

    def getAllCurricula(self):
        return self.curricula

    def getAllConstraints(self):
        return self.constraints



class DictData(IData):
    courses = {}
    rooms = {}
    curricula = {}
    constraints = {}
    constraintsPeriods = {}

    curriculumLookup = {}

    """ convert old data object """
    def __init__(self, data):
        self.periodsPerDay, self.instanceName, self.daysNum = data.periodsPerDay, data.instanceName, data.daysNum
        for c in data.courses:
            self.courses[c.id] = c
        for r in data.rooms:
            self.rooms[r.id] = r

        self.curriculumLookup = {c.id: set() for c in data.getAllCourses()}

        for c in data.curricula:
            self.curricula[c.id] = c
            for m in c.members:
                self.curriculumLookup[m].add(c)

        self.constraints = { c.id: [] for c in data.constraints}
        self.constraintsPeriods = { c.id: [] for c in data.constraints}
        for c in data.constraints:
            self.constraints[c.id].append(c)
            self.constraintsPeriods[c.id].append(c.day * self.periodsPerDay + c.dayPeriod)





    def getAllCourses(self):
        return self.courses.values()
    def getAllRooms(self):
        return self.rooms.values()
    def getAllCurricula(self):
        return self.curricula.values()
    def getAllConstraints(self):
        return sum(self.constraints.values(),[])
    def getAllCourseIds(self):
        return self.courses.keys()



    def getCourse(self, id):
        return self.courses[id]
    def getRoom(self, id):
        return self.rooms[id]
    def getCurriculum(self, id):
        return self.curricula[id]
    def getConstraintsForCourse(self, id):
        if id in self.constraints.keys():
            return self.constraints[id]
        else:
            return []

    def getCurriculumForCourseId(self, courseId):
        return self.curriculumLookup[courseId] if courseId in self.curriculumLookup else set()

    def getConstraintsOnlyKeysForCourse(self, id):
        if id in self.constraintsPeriods.keys():
            return self.constraintsPeriods[id]
        else:
            return []


    def popCourse(self, id):
        self.courses[id].assignedLectureNum+=1


    def getUnfinishedCourses(self):
        return filter(lambda x: x.lectureNum>x.assignedLectureNum, self.getAllCourses())

    def getRandomCourse(self):
        courseId = random.choice(self.courses.keys())
        return self.courses[courseId]

    def getBestRoom(self, roomIdList):
        roomList = filter(lambda x : x.id in roomIdList, self.getAllRooms())
        return min(roomList, key = lambda x : x.capacity)

    def clearAssignedLectures(self, coursesList):
        for course in coursesList:
            course.assignedLectureNum = 0

    def getAllLecturesCount(self):
        lecturesSum = 0
        for course in self.getAllCourses():
            lecturesSum += self.getCourse(course.id).lectureNum

        return lecturesSum

