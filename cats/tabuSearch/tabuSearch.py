import itertools
from cats.utils.inputDataStructures import Course, Room, Constraint, Curriculum

class TimeTable(object):
    def __init__(self, daysNum, periodsPerDayNum):
	    # courseId roomId
    	self.periodsPerDayNum = periodsPerDayNum
        self.daysNum = daysNum
        self.slot = []
        self.timeSlots = range(self.daysNum * self.periodsPerDayNum)
        self.timeTable = {x : [] for x in self.timeSlots}
        self.neighbourhoodList = {}

    def getTimeTable(self):
        return self.timeTable

    """Get value of slot from timetable"""
    def getValueSlot(self, day, day_period):
        key = day * self.periodsPerDayNum + day_period
        return self.timeTable[key]

    """Create neighourhood list for courses regarding regarding curriculum lists"""
    def createNeighbourhoodList(self, curriculumList, courseList):
        self.neighbourhoodList = {x.id : set([]) for x in courseList}
        for c in curriculumList:
            comb = []
            comb += itertools.combinations(c.members, 2)
            for i in comb:
                self.neighbourhoodList[i[0]].add(i[1])
                self.neighbourhoodList[i[1]].add(i[0])
        return self.neighbourhoodList

    def getKey(self, day, day_period):
        key = day * self.periodsPerDayNum + day_period
        return key

    def mapKeys(self,constraint):
        key = self.getKey(constraint.day, constraint.dayPeriod)
        return key

    def getKeyConstraintsOfCourse(self, constraintsList, courseId):
        keysConstraintsOfCourse = map(self.mapKeys, [ x for x in constraintsList if x.id == courseId])
        return keysConstraintsOfCourse

    """Count number of available slots for course TODO : consider neighourhood"""
    def availableNumberOfPeriods(self, constraintsList, courseId):
        keysConstraintsOfCourse = set(self.getKeyConstraintsOfCourse(constraintsList, courseId))
        availableSlots = set(filter(lambda x: self.timeTable[x] == self.slot, self.timeTable))
        counter = len(availableSlots - keysConstraintsOfCourse)
        return counter

