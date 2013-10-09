class Timetable(object):
    """Store timetable"""

    def __init__(self, daysNum, periodsPerDayNum):
        self.days = []
        for i in range(daysNum):
            self.days.append([])


