from cats.utils.inputDataStructures import Course, Room, Constraint, Curriculum

class TimeTable(object):
    def __init__(self, daysNum, periodsPerDayNum):
	    # courseId roomId
    	self.periodsPerDayNum = periodsPerDayNum
        self.daysNum = daysNum
        self.slot = []
        self.timeSlots = range(self.daysNum * self.periodsPerDayNum)
        self.timeTable = dict()
        for key in self.timeSlots:
            self.timeTable[key] = self.slot

    def getTimeTable(self):
        return self.timeTable

    """Get value of slot from timetable"""
    def getValueSlot(self, day, day_period):
        key = day * self.periodsPerDayNum + day_period
        return self.timeTable[key]

    def getKey(self, day, day_period):
        key = day * self.periodsPerDayNum + day_period
        return key

    def mapKeys(self,constraint):
        key = self.getKey(constraint.day, constraint.dayPeriod)
        return key

    def getKeyConstraintsOfCourse(self, constraintsList, courseId):
        keysConstraintsOfCourse = map(self.mapKeys, [ x for x in constraintsList if x.id == courseId])
        return keysConstraintsOfCourse

    """Count number of available slots for course"""
    def availableNumberOfPeriods(self, constraintsList, courseId):
        keysConstraintsOfCourse = set(self.getKeyConstraintsOfCourse(constraintsList, courseId))
        availableSlots = set(filter(lambda x: self.timeTable[x] == self.slot, self.timeTable))
        counter = len(availableSlots - keysConstraintsOfCourse)
        return counter

