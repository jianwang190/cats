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

    curriculumLookup = {}

    """ convert old data object """
    def __init__(self, data):
        self.periodsPerDay, self.instanceName, self.daysNum = data.periodsPerDay, data.instanceName, data.daysNum
        for c in data.courses:
            self.courses[c.id] = c
        for r in data.rooms:
            self.rooms[r.id] = r
        for c in data.curricula:
            self.curricula[c.id] = c
            for m in c.members:
                self.curriculumLookup.setdefault(m, []).append(c)

        self.constraints = { c.id: [] for c in data.constraints}
        for c in data.constraints:
            self.constraints[c.id].append(c)





    def getAllCourses(self):
        return self.courses.values()
    def getAllRooms(self):
        return self.rooms.values()
    def getAllCurricula(self):
        return self.curricula.values()
    def getAllConstraints(self):
        return sum(self.constraints.values(),[])



    def getCourse(self, id):
        return self.courses[id]
    def getRoom(self, id):
        return self.rooms[id]
    def getCurriculum(self, id):
        return self.curricula[id]
    def getConstraintsForCourse(self, id):
        return self.constraints[id]

    def getCurriculumForCourseId(self, courseId):
        return self.curriculumLookup[courseId] if courseId in self.curriculumLookup else []


    def popCourse(self, id):
        self.courses[id].assignedLectureNum+=1

    def getUnfinishedCourses(self):
        return filter(lambda x: x.lectureNum>x.assignedLectureNum, self.getAllCourses())