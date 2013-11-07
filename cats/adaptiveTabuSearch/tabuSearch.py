import operator
from cats.adaptiveTabuSearch import softConstraints2
"""Tabu search algorithm"""
"""Period related costs - sum(minimumWorkingDays, curriculumCompactness)"""
"""Room related costs - sum(roomCapacity, roomStability)"""

PERIOD_RELATED_COST_TAU = 2
DEPTH_OF_TABU_SEARCH = 10


class Move(object):
    def __init__(self, period, roomId):
        self.period = period
        self.room = roomId


# separate object of TabuList class should be created for N1 and N2
class TabuList(object):
    """"Contain tabu moves in tabuList"""
    def __init__(self, courseList, neighborhoodList):
        self.tabuList = {x.id : [] for x in courseList}
        self.parameter = self.coefficientTabuTenure(courseList, neighborhoodList)

    def addTabuMove(self, courseId, period, roomId):
        move = Move(period, roomId)
        self.tabuList[courseId].append(move)


    def coefficientTabuTenure(self, courseList, neighborhoodList):
        """
        Function to count coefficient for tabu tenure (number of conflicting courses / total number of courses)
        :param courseList: list of course ids
        :param neighborhoodList:neighborhood list for courses
        :return: dictionary with coefficient for each courseId
        """
        totalNumberOfCourses = len(courseList)
        parameter = {x.id : [] for x in courseList}

        map(lambda x : parameter[x].append(float(len(neighborhoodList[x])) / float(totalNumberOfCourses)), neighborhoodList)
        return parameter

    """Tabu tenure of courseId is tuned adaptively according to the current solution quality f and moving frequency"""
    def tabuTenure(self, courseId, partialTimetable, data):
        """Moving frequency of lectures of courseId"""
        movingFreqCourse = len(self.tabuList[courseId])
        f = softConstraints2.totalSoftConstraintsForTimetable(partialTimetable, data)
        tt =  f + self.parameter[courseId][0] * movingFreqCourse
        return tt


def matchingRoomAllocations(timetable, slot, data, sortedRoomIdList):
    """
    Matching algorithm to make room allocations (number of courses in slot <= number of rooms)
    Match rooms to courses starting from courses with the biggest number of students, match the biggest available room
    :param timetable: timetable to which assigned rooms ids
    :param slot: slot to which assign rooms
    :param data: data to tested example
    :param sortedRoomIdList: sorted list of rooms regarding to capacity
    :return: timetable for slot with assigned rooms for each course
    """
    studentsForCourse= {x.courseId: data.getCourse(x.courseId).studentsNum for x in timetable[slot]}
    sortedStudentsForCourse = sorted(studentsForCourse.iteritems(), key=operator.itemgetter(1), reverse=True)
    for x in timetable[slot]:
        indexOfRoom = map(operator.itemgetter(0), sortedStudentsForCourse).index(x.courseId)
        x.roomId = sortedRoomIdList[indexOfRoom].id

    return timetable[slot]













