class Model(object):
    def getId(self):
        return self.meta["id"]

class Course(Model):
    def __init__(self, id, teacher, lectureNum, minWorkingDays, studentsNum, typeOfRoom = ''):
        self.id = id
        self.teacher = teacher
        self.lectureNum = lectureNum
        self.minWorkingDays = minWorkingDays
        self.studentsNum = studentsNum
        self.typeOfRoom = typeOfRoom
        self.assignedLectureNum = 0
class Room(Model):
    def __init__(self, id, capacity, type=None):
        self.id = id
        self.capacity = capacity
        self.type = type
    def __str__(self):
        return str(self.id)+" "+str(self.capacity)

class Curriculum(Model):
    def __init__(self, id, courseNum, members):
        self.id = id
        self.courseNum = courseNum
        self.members = members

class Constraint(Model):
    def __init__(self, id, day, dayPeriod):
        self.id = id
        self.day = day
        self.dayPeriod = dayPeriod
