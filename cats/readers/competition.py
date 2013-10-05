# -*- coding: utf-8 -*-
import os
import re

class Reader(object):

    def __init__(self):
        self.courses = []
        self.rooms = []
        self.curricula = []
        self.constraints = []

    def getInstanceName(self):
        return self.meta["name"]
    def getCoursesNum(self):
        return self.meta["courses"]
    def getRoomsNum(self):
        return self.meta["rooms"]
    def getDaysNum(self):
        return self.meta["days"]
    def getPeriodsPerDayNum(self):
        return self.meta["periods_per_day"]
    def getCurriculumNum(self):
        return self.meta["curricula"]
    def getConstraintNum(self):
        return self.meta["constraints"]


class CompetitionReader(Reader):
    def __init__(self, instanceNum):
        Reader.__init__(self)
        self.meta = {}
        print os.getcwd()
        with open(u"data/Curriculum_based_Course_timetabling/datasets/comp" + str(instanceNum) + ".ctt") as f:
            buffer = map(lambda x: re.sub("\\\n", "", x), f.readlines())
            it = 0
            while it<len(buffer):
                s = buffer[it].split(':')
                if len(s)<2:
                    break
                if s[0].lower() == "name":
                    self.meta[s[0].lower()] = s[1].strip()
                else:
                    self.meta[s[0].lower()] = int(s[1])
                it+=1

            it+=2
            while it<len(buffer):
                s = buffer[it].split(' ')
                if len(s)<5:
                    break
                self.courses.append(Course(s[0], s[1], s[2], s[3], s[4]))
                it+=1

            it+=2
            while it<len(buffer):
                s = re.split("\W", buffer[it])
                if len(s)<2:
                    break
                self.rooms.append(Room(s[0], s[1]))
                it+=1
            it+=2
            while it<len(buffer):
                s = re.split("\W", buffer[it])
                if len(s)<3:
                    break
                self.curricula.append(Curriculum(s[0], s[1], s[2:]))
                it+=1
            it+=2
            while it<len(buffer):
                s = re.split("\W", buffer[it])
                if len(s)<3:
                    break
                self.constraints.append(Constraint(s[0], s[1], s[2]))
                it+=1

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
