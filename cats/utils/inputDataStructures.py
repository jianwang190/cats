class Model(object):
    def getId(self):
        return self.meta["id"]

class Course(Model):
    def __init__(self, id, teacher, lectureNum, minWorkingDays, studentsNum):
        self.id = id
        self.teacher = teacher
        self.lectureNum = lectureNum
        self.minWorkingDays = minWorkingDays
        self.studentsNum = studentsNum

class Room(Model):
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity

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
