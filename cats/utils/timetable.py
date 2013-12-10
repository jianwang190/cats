import collections, json, random
from itertools import combinations, groupby
import sys
from cats.ga.checkHardConstraints import checkHardConstraintsForSlots


class TimeTableFactory(object):
    @classmethod
    def getTimeTable(self, data):
        """
        Cell in timetable format : tuples (courseId, roomId) instead of old CellOfTimeTable
        :param data:
        :return: timetable
        """
        t = TimeTable()
        t.periodsPerDay = data.periodsPerDay
        t.daysNum = data.daysNum
        t.timeSlots = range(t.daysNum * t.periodsPerDay)
        t.timeTable = {x : [] for x in t.timeSlots}
        t.neighbourhoodList = t.createNeighbourhoodList(data.getAllCurricula(), data.getAllCourses())
        t.roomsIdListForCourses = t.getRoomsIdForCourses(data.getAllRooms(), data.getAllCourses())
        t.assignedLecturesSum = 0
        return t


class TimeTable(object):
    def copy(self):
        other = TimeTable()
        other.periodsPerDay, other.daysNum, other.timeSlots = self.periodsPerDay, self.daysNum, self.timeSlots
        other.timeTable = {x: self.getTimeTable()[x][:] for x in self.getTimeTable().keys()}
        other.neighbourhoodList = self.neighbourhoodList
        other.roomsIdListForCourses = self.roomsIdListForCourses
        return other


    def getTimeTable(self):
        return self.timeTable

    def getValueSlot(self, day, day_period):
        """
        Get value of slot from timetable
        :param day: day
        :param day_period: period in day
        :return:
        """
        key = day * self.periodsPerDay + day_period
        return self.timeTable[key]


    def createNeighbourhoodList(self, curriculumList, courseList):
        """
        Create neighborhood list for courses regarding regarding curriculum lists and teacher's conflicts
        :param curriculumList:
        :param courseList:
        :return:
        """
        self.neighbourhoodList = {x.id : set([]) for x in courseList}
        for c in curriculumList:
            comb = combinations(c.members, 2)
            for i in comb:
                self.neighbourhoodList[i[0]].add(i[1])
                self.neighbourhoodList[i[1]].add(i[0])

        courseList.sort(key= lambda x: x.teacher)
        for k, teacherCourses in groupby(courseList, key=lambda x: x.teacher):
            comb = combinations([e.id for e in teacherCourses], 2)
            for i in comb:
                self.neighbourhoodList[i[0]].add(i[1])
                self.neighbourhoodList[i[1]].add(i[0])

        return self.neighbourhoodList

    def getKey(self, day, day_period):
        """
        Get key to slot in timetable
        :param day: day
        :param day_period: period in day
        :return: key in timetable
        """
        key = day * self.periodsPerDay + day_period
        return key

    def getPeriodPair(self, slot):
        """
        Converts a timeslot value to a pair of day and the day's period
        :param slot:
        :return: [ day , day_period ]
        """
        return [(slot/self.periodsPerDay), (slot%self.periodsPerDay)]

    def mapKeys(self, constraint):
        """
        Map day and period to key in timetable
        :param constraint: constraints
        :return: key
        """
        key = self.getKey(constraint.day, constraint.dayPeriod)
        return key

    def getAllSlots(self):
        return self.timeSlots

    def createListOfRooms(self, roomList, course):
        """
        Create list of rooms for course with appropriate capacity of room for course (considering number of students attending course)
        :param roomList: list of rooms
        :param courseStudentsNum: number of students attending to course
        :return:
        """
        listOfRooms = set([r.id for r in roomList if (r.capacity >= course.studentsNum and \
                                                      (course.typeOfRoom == None or r.type == course.typeOfRoom))])
        return listOfRooms

    """Get rooms ids for each of courses (considering number of students)"""
    def getRoomsIdForCourses(self, roomList, courseList):
        roomsForCourses = {x.id: self.createListOfRooms(roomList, x) for x in courseList}
        return roomsForCourses

    """Get list of constraints for course"""
    def getKeyConstraintsOfCourse(self, constraintsList, courseId):
        keysConstraintsOfCourse = map(self.mapKeys, [ x for x in constraintsList if x.id == courseId])
        return keysConstraintsOfCourse

    """Check if slot is available for course, considering neighbourhood (conflicts courses)"""
    def checkIfAvailable(self, timeTableList, courseId):
        rooms = set()
        for cell in timeTableList:
            if (cell is not []) and ((cell[0] in self.neighbourhoodList[courseId]) or (cell[0] == courseId)):
                return {'period' : False, 'unavailableRooms' : set()}
            else:
                rooms.update(cell[1])
        return {'period': True, 'unavailableRooms' : rooms}


    """Count number of available slots for course, function considers neighourhood, count available positions - periods (slot, room)"""
    """availablePeriodsNum - the total number of available periods for course, availablePeriods - list of available periods"""
    """availablePairsNum - the total number of available positions (period and room pairs), availablePairs - list of available pairs (period- room)"""
    def availablePeriodsRooms(self, constraintsList, courseId):
        keysConstraintsOfCourse = set(self.getKeyConstraintsOfCourse(constraintsList, courseId))

        availablePeriods = set()
        availablePairs = {}
        for slot in self.timeSlots:
            result = self.checkIfAvailable(self.timeTable[slot], courseId)
            if((result['period'] == True) and (slot not in keysConstraintsOfCourse)):
                availablePeriods.add(slot)
                availablePairs[slot] = self.roomsIdListForCourses[courseId] - result['unavailableRooms']
        availablePairsNum = sum([len(availablePairs[x]) for x in availablePairs])

        return {'availablePeriodsNum' : len(availablePeriods), \
                'availablePairsNum': availablePairsNum, \
                'availablePeriods' : availablePeriods, \
                'availablePairs' : availablePairs }

    def availableSlotRoomPairs(self, data, courseId):
        rooms = dict()
        for slot in self.getTimeTable().keys():
            rooms[slot] = self.availableRoomsList(slot, data, courseId)
        possibleSlots = self.availableSlotsForCourse(data, courseId)
        pairs = dict()
        for slot in possibleSlots:
            if len(rooms[slot]) > 0:
                pairs[slot] = rooms[slot]

        return pairs


    def availableSlotsForCourse(self, data, courseId):
        bannedSlots = list()
        for constraint in data.getConstraintsForCourse(courseId):
            bannedSlots.append(self.getKey(constraint.day, constraint.dayPeriod))
        possibleSlots = list(set(self.getAllSlots()) - set(bannedSlots))
        bannedSlots = list()
        for slot in possibleSlots:
            for lecture in self.getTimeTable()[slot]:
               if lecture[0] in self.neighbourhoodList[courseId]:
                   bannedSlots.append(slot)
                   continue
        possibleSlots = list(set(possibleSlots) - set(bannedSlots))

        return possibleSlots

    def assignedLectures(self, courseId):
        sum = []
        for slot, cells in self.getTimeTable().iteritems():\
            sum += filter(lambda x: x[0] == courseId, cells)
        return sum
        
    def assignedLecturesWithSlots(self, courseId):
        sum = dict()
        for slot, cells in self.getTimeTable().iteritems():
            sum[slot] = filter(lambda x: x[0] == courseId, cells)
        return filter(lambda x : len(x[1]) > 0, sum.iteritems())

    def getAssignedDays(self, courseId):
        lectures = self.assignedLecturesWithSlots(courseId)
        assignedDays = map(lambda x : self.getPeriodPair(x[0])[0], lectures)

        return set(assignedDays)

    def getAssignedLecturesSum(self, data):
        """
        Counts the number of lectures currently assigned in this timeTable
        :return: amount of lectures
        """
        lecturesSum = 0
        for slot in self.getTimeTable().keys():
            lecturesSum += len(self.getTimeTable()[slot])

        return lecturesSum

    def readLecturesToTimetable(self, path):
        f = open(path, "r")
        lecturesBuffer = map(lambda x: x.rstrip('\n'), f.readlines())
        for lecture in lecturesBuffer:
            l = lecture.split()
            #courseId l[1], roomId l[2]
            self.timeTable[int(l[0])].append((l[1], l[2]))

    """ returns number of conflicting courses """
    """ assumes all conflicts are stored in neighbourhoodList """
    def conflictingCourses(self, courseId):
        return len(self.neighbourhoodList[courseId])
    
    def unavailableUnfinishedCoursesLectureNum(self, period, courseId, data):
        result = 0
        for course in data.getUnfinishedCourses():
            if self.neighbourhoodList.has_key(courseId) and \
                course.id in self.neighbourhoodList[courseId]:
                result += course.lectureNum - course.assignedLectureNum
        return result
    
    def availableRoomsList(self, period, data, courseId):
        allAvailableRooms = list(set(map(lambda x: data.rooms[x].id, \
                                         filter(lambda r: data.courses[courseId].typeOfRoom == None or \
                                                          data.rooms[r].type == data.courses[courseId].typeOfRoom, data.rooms))) \
               - set(map(lambda x: x[1], self.getTimeTable()[period])))
        return allAvailableRooms
    
    def allAvailableRoomsList(self, period, data):
        return list(set(map(lambda x: x.id, data.getAllRooms())) \
               - set(map(lambda x: x[1], self.getTimeTable()[period])))


    def addDataToTimetable(self, assignedList):
        """
        Add data to timetable (period, courseId, roomId, curId - optional)
        :param assignedList: courses and rooms to add to timetable
        """
        map(lambda a: self.timeTable[a[0]].append((a[1],a[2])), assignedList)

    def removeFromTimetable(self, assignedList):
        map(lambda a: self.timeTable[a[0]].remove((a[1], a[2])), assignedList)


    def serialize(self, data, path=None):
        if path is not None:
            sys.stdout = open(path, 'w')
        for p in self.getTimeTable().keys():
            for c in self.getTimeTable()[p]:
                print " ".join((c[0], c[1], str(p/data.periodsPerDay), str(p%data.periodsPerDay)+'\n'))

    def jsonify(self):
        """
        Serialize timetables neighbourhood list to json, d3.js readable
        Check http://bl.ocks.org/mbostock/4062045
        """
        links = []
        nodes = self.neighbourhoodList.keys()
        for n in nodes:
            for m in self.neighbourhoodList[n]:
                links.append({"source": nodes.index(n), "target": nodes.index(m), "value": 1})
        print json.dumps({"nodes" : map(lambda x: {"name": x, "group": 1}, self.neighbourhoodList.keys()), "links": links}, \
                         indent=4, separators=(',', ': '))

    def copySolution(self, data):
        newSolution = TimeTableFactory.getTimeTable(data)
        for slot in self.getTimeTable().keys():
            for lecture in self.getTimeTable()[slot]:
                newSolution.getTimeTable()[slot].append(lecture)

        return newSolution

    def checkIfInsertionIsValid(self, slot, courseId, roomId, data):
        #remove a random lecture of a course at first
        oldLecture = random.choice(self.assignedLecturesWithSlots(courseId))
        self.removeFromTimetable([(oldLecture[0], oldLecture[1][0][0], oldLecture[1][0][1])])

        initialPenalty = checkHardConstraintsForSlots(self, data, [slot])
        self.addDataToTimetable([(slot, courseId, roomId)])
        if checkHardConstraintsForSlots(self, data, [slot]) <= initialPenalty:
            return True
        else:
            self.addDataToTimetable([(oldLecture[0], oldLecture[1][0][0], oldLecture[1][0][1])])
            return False

    def saveResultsToFile(self, fileName):
        f = open(fileName,'w')
        for slot in self.getTimeTable().keys():
            for lecture in self.getTimeTable()[slot]:
                line = lecture[0] + ' ' + lecture[1] + ' ' + str(self.getPeriodPair(slot)[0]) + ' ' + \
                       str(self.getPeriodPair(slot)[1]) + '\n'
                f.write(line)
        f.close()
