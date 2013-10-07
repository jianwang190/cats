class Data(object):
    """Store data"""

    def __init__(self):
        self.courses = []
        self.rooms = []
        self.curricula = []
        self.constraints = []
        self.instanceName = ""
        self.daysNum = 0
        self.periodsPerDayNum = 0

    def getCoursesNum(self):
        """Return number of courses"""
        return len(self.courses)

    def getRoomsNum(self):
        """Return number of rooms"""
        return len(self.rooms)

    def getCurriculumNum(self):
        """Return number of curriculum"""
        return len(self.curricula)

    def getConstraintNum(self):
        """Return number of constraints"""
        return len(self.constraints)





