class EvaluationFunction(object):
    """Store evaluation functions"""
    def __init__(self, data, factory):
        self.data = data
        self.factory = factory

    def evaluate(self, timetable):
        """Return sum of penalties"""

        #print "------------------------"

        penalty = self.countRoomCapacityPenalty(timetable)
        penalty += self.countMinimumWorkingDaysPenalty(timetable)
        penalty += self.countCurriculumCompactnessPenalty(timetable)
        penalty += self.countRoomStabilityPenalty(timetable)
        penalty += self.countConflictsPenalty(timetable)
        penalty += self.countAvailabilitesPenalty(timetable)

        #print "------------------------"
        return penalty

    def countRoomCapacityPenalty(self, timetable):
        """Return sum of penalties for room capacity"""
        penalty = 0
        for day in range(len(timetable.periods)):
            for period in range(len(timetable.periods[day])):
                for room in self.data.rooms:
                    course = timetable.periods[day][period][room.id]
                    if course != None:
                        if room.capacity < course.studentsNum:
                            penalty += course.studentsNum - room.capacity

        #print penalty
        return penalty

    def countMinimumWorkingDaysPenalty(self, timetable):
        """Return sum of penalties for minimum  working days"""
        penalty = 0

        for course in self.data.courses:
            days = set()
            for slot in timetable.courses[course.id]:
                day, _, _ = self.factory.unzip(slot)
                days.add(day)

            if len(days) < course.minWorkingDays:
                penalty += (course.minWorkingDays - len(days)) * 5

        #print penalty
        return penalty

    def countCurriculumCompactnessPenalty(self, timetable):
        """Return sum of penalties for curriculum compactness"""
        penalty = 0
        for curriculum in self.data.curricula:
            for day in timetable.periods:
                penaltyDay =0
                existOne = False
                for period in day:
                    wasInPrevousPeriod = False
                    for room in period:
                        course = period[room]
                        if course != None:
                            if course.id in curriculum.members:
                                if existOne and not wasInPrevousPeriod:
                                    penaltyDay += 2
                                existOne = True
                                wasInPrevousPeriod = True
                if penaltyDay > 0:
                    penalty += penaltyDay + 2


        #print penalty
        return penalty

    def countRoomStabilityPenalty(self, timetable):
        """Return sum of penalties for room stability"""
        penalty = 0

        for course in self.data.courses:
            rooms = set()
            for slot in timetable.courses[course.id]:
                _, _, room = self.factory.unzip(slot)
                rooms.add(room.id)

            if len(rooms) > 1:
                penalty += len(rooms) - 1

        return penalty

    def countConflictsPenalty(self, timetable):
        """Return sum of penalties for conflicts"""
        penalty = 0

        for day in range(len(timetable.periods)):
            for period in range(len(timetable.periods[day])):
                teachers = dict()
                for room in self.data.rooms:
                    course = timetable.periods[day][period][room.id]
                    if course != None:
                        teachers[course.teacher] = teachers.get(course.teacher, 0) + 1
                for t in teachers:
                    if teachers[t] > 1:
                        penalty += (teachers[t] * (teachers[t] -1)) / 2

        for day in range(len(timetable.periods)):
            for period in range(len(timetable.periods[day])):
                for curriculum in self.data.curricula:
                    count = 0
                    for room in self.data.rooms:
                        course = timetable.periods[day][period][room.id]
                        if course in curriculum.members:
                            count += 1
                    penalty += (count * (count -1)) / 2
        return penalty * 1000000

    def countAvailabilitesPenalty(self, timetable):
        """return sum of penalties for availabilities"""
        penalty = 0

        for constraint in self.data.constraints:
            day = constraint.day
            period = constraint.dayPeriod
            for room in self.data.rooms:
                course = timetable.periods[day][period][room.id]
                if course != None:
                    if course.id == constraint.id:
                        penalty +=1

        return penalty * 1000000


