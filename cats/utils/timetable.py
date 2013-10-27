import itertools
from cats.utils.data import Data

class CellOfTimeTable(object):
    def __init__(self, courseId = [], roomId = [], curriculumId = []):
        self.courseId = courseId
        self.roomId = roomId
        self.curriculumId = curriculumId

class TimeTableFactory(object):
    @classmethod
    def getTimeTable(self, data):
        t = TimeTable()
        t.periodsPerDay = data.periodsPerDay
        t.daysNum = data.daysNum
        t.timeSlots = range(t.daysNum * t.periodsPerDay)
        t.timeTable = {x : [] for x in t.timeSlots}
        t.neighbourhoodList = t.createNeighbourhoodList(data.curricula, data.courses)
        t.roomsIdListForCourses = t.getRoomsIdForCourses(data.rooms, data.courses)


        return t


class TimeTable(object):
    def getTimeTable(self):
        return self.timeTable

    """Get value of slot from timetable"""
    def getValueSlot(self, day, day_period):
        key = day * self.periodsPerDay + day_period
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

    """Get key to slot in timetable"""
    def getKey(self, day, day_period):
        key = day * self.periodsPerDay + day_period
        return key

    """Map day and period to key in timetable"""
    def mapKeys(self,constraint):
        key = self.getKey(constraint.day, constraint.dayPeriod)
        return key

    """Create list of rooms for course with appropriate capacity of room for course (considering number of students attending course)"""
    def createListOfRooms(self, roomList, courseStudentsNum):
        listOfRooms = set([r.id for r in roomList if (r.capacity >= courseStudentsNum)])
        return listOfRooms

    """Get rooms ids for each of courses (considering number of students)"""
    def getRoomsIdForCourses(self, roomList, courseList):
        roomsForCourses = {x.id: self.createListOfRooms(roomList, x.studentsNum) for x in courseList}
        return roomsForCourses

    """Get list of constraints for course"""
    def getKeyConstraintsOfCourse(self, constraintsList, courseId):
        keysConstraintsOfCourse = map(self.mapKeys, [ x for x in constraintsList if x.id == courseId])
        return keysConstraintsOfCourse

    """Check if slot is available for course, considering neighbourhood (conflicts courses)"""
    def checkIfAvailable(self, timeTableList, courseId):
        rooms = set()
        for cell in timeTableList:
            if (cell is not []) and ((cell.courseId in self.neighbourhoodList[courseId]) or (cell.courseId == courseId)):
                return {'period' : False, 'unavailableRooms' : set()}
            else:
                rooms.update(cell.roomId)
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

    def assignedLectures(self, courseId):
        sum = []
        for slot, cells in self.getTimeTable().iteritems():
            sum += filter(lambda x: x.courseId == courseId, cells)
        return sum

    """ returns number of conflicting courses """
    """ assumes all conflicts are stored in neighbourhoodList """
    def conflictingCourses(self, courseId):
        return len(self.neighbourhoodList[courseId])

    """Add data to timetable (period, courseId, roomId, curId - optional)"""
    def addDataToTimetable(self, assignedList):
        for a in assignedList:
            if(len(a) < 4):
                self.timeTable[a[0]].append(CellOfTimeTable(a[1],a[2]))
            else:
                self.timeTable[a[0]].append(CellOfTimeTable(a[1],a[2],a[3]))