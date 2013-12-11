class Model(object):
    def getId(self):
        return self.meta["id"]

class Course(Model):
    """
    Class containing data about whole courses

    """
    def __init__(self, id, teacher = '', lectureNum = 0, minWorkingDays = 0, studentsNum = 0, nameOfSubject = ''):
        self.id = id
        self.teacher = teacher
        self.lectureNum = lectureNum
        self.minWorkingDays = minWorkingDays
        self.studentsNum = studentsNum
        self.assignedLectureNum = 0
        self.nameOfSubject = nameOfSubject

class Room(Model):
    """
    structure containing information about rooms
    type n- normal room, type e - exercise, type , type l - library, type o - outside school, w - workshops, c - computer

    """
    def __init__(self, id, capacity = 0, type = ''):
        self.id = id
        self.capacity = capacity
        self.type = type
    def __str__(self):
        return str(self.id)+" "+str(self.capacity)+" "+str(self.type)

class Curriculum(Model):
    """
    Class containing all curriculum

    """
    def __init__(self, id, studentsNumber = 0):
        self.id = id
        self.studentsNumber = studentsNumber
        self.courseNum = 0
        self.members = []

class Constraint(Model):
    def __init__(self, id, day, dayPeriod):
        self.id = id
        self.day = day
        self.dayPeriod = dayPeriod
