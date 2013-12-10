class EvaluationFunction(object):
    """Store evaluation functions"""
    def __init__(self, data, factory):
        self.data = data
        self.factory = factory

    def evaluate(self, timetable):
        """Return sum of penalties"""

        penalty = self.countRoomCapacityPenalty(timetable)
        penalty += self.countMinimumWorkingDaysPenalty(timetable)
        penalty += self.countCurriculumCompactnessPenalty(timetable)
        penalty += self.countRoomStabilityPenalty(timetable)
        penalty += self.countConflictsPenalty(timetable)
        penalty += self.countLectureConflictsPenalty(timetable)
        penalty += self.countAvailabilitesPenalty(timetable)

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
                            #print day,period,room.id,course.id
                            #print room.capacity, course.studentsNum
                            penalty += course.studentsNum - room.capacity
        #print "Room capacity: ",penalty
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
                #print course.id
                penalty += (course.minWorkingDays - len(days)) * 5

        #print "Min working days: ",penalty
        return penalty

    def countCurriculumCompactnessPenalty(self, timetable):
        """Return sum of penalties for curriculum compactness"""
        penalty = 0
        for curriculum in self.data.curricula:
            for day in range(len(timetable.periods)):
                for period in range(len(timetable.periods[day])):
                    for room in self.data.rooms:
                        course = timetable.periods[day][period][room.id]
                        if course != None:
                            if course.id in curriculum.members:
                                ce = course
                                before = False
                                if period == 0:
                                    before = False
                                else:
                                    for room in self.data.rooms:
                                        course = timetable.periods[day][period-1][room.id]
                                        if course != None:
                                            if course.id in curriculum.members:
                                                before = True

                                after = False
                                if period == len(timetable.periods[day]) -1:
                                    after = False
                                else:
                                    for room in self.data.rooms:
                                        course = timetable.periods[day][period+1][room.id]
                                        if course != None:
                                            if course.id in curriculum.members:
                                                after = True
                                if not before and not after:
                                    #print day, period, curriculum.id, ce.id
                                    penalty += 2


        #for curriculum in self.data.curricula:
            #for day in timetable.periods:
                #print "Day"
                #penaltyDay =0
                #prev = False
                #alone = False
                #per = 0
                #for period in day:
                    #print "Day"
                    #for room in period:
                        #course = period[room]
                        #if course != None:
                            #if course.id in curriculum.members:
                                #if prev == False or per -1 != prev:
                                    #penaltyDay += 2
                                    #alone = True
                                    #print course.id
                                #else:
                                    #if alone:
                                        #print "Del ", course.id
                                        #penaltyDay -= 2
                                    #alone = False
                                #prev = per
                    #per += 1
                #if penaltyDay > 0:
                    #penalty += penaltyDay


        #print "Curiculum compactness: ",penalty
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
                #print course.id
                #print len(rooms)
                penalty += len(rooms) - 1

        #print "Room stability:  ",penalty
        return penalty

    def countLectureConflictsPenalty(self, timetable):
        """Return sum of penalties for lecture conflicts"""
        penalty = 0

        for day in range(len(timetable.periods)):
            for period in range(len(timetable.periods[day])):
                courses = dict()
                for room in self.data.rooms:
                    course = timetable.periods[day][period][room.id]
                    if course != None:
                        courses[course.id] = courses.get(course.id, 0) + 1
                for c in courses:
                    if courses[c] > 1:
                        #print c
                        penalty += courses[c] - 1
        #print "Lecture Conflicts: ", penalty
        return 1000000 * penalty

    def countConflictsPenalty(self, timetable):
        """Return sum of penalties for conflicts"""
        penalty = 0

        for day in range(len(timetable.periods)):
            for period in range(len(timetable.periods[day])):
                teachers = dict()
                courses = set()
                for room in self.data.rooms:
                    course = timetable.periods[day][period][room.id]
                    if course != None:
                        if not course.id in courses:
                            teachers[course.teacher] = teachers.get(course.teacher, 0) + 1
                            #if teachers[course.teacher] > 1:
                                #print day, period
                        courses.add(course.id)


                for t in teachers:
                    if teachers[t] > 1:
                        #print t
                        penalty += (teachers[t] * (teachers[t] -1)) / 2

        for day in range(len(timetable.periods)):
            for period in range(len(timetable.periods[day])):
                for curriculum in self.data.curricula:
                    count = 0
                    courses = set()
                    for room in self.data.rooms:
                        course = timetable.periods[day][period][room.id]
                        if course != None:
                            if course.id in curriculum.members:
                                count += 1
                                courses.add(course.id)
                    if len(courses) > 1:
                        #print day, period
                        #print courses
                        count = len(courses)
                        #print (count * (count -1)) / 2
                        penalty += (count * (count -1)) / 2
                        #print penalty
        #print "Conflicts: ", penalty
        return penalty * 1000000

    def countAvailabilitesPenalty(self, timetable):
        """return sum of penalties for availabilities"""
        penalty = 0

        #print "Avail"

        for constraint in self.data.constraints:
            day = constraint.day
            period = constraint.dayPeriod
            for room in self.data.rooms:
                course = timetable.periods[day][period][room.id]
                if course != None:
                    if course.id == constraint.id:
                        #print course.id, day, period
                        penalty +=1

        #print "Avail: ", penalty
        return penalty * 1000000


