import operator
from cats.adaptiveTabuSearch import softConstraints
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
        self.parameter = self.coeficientTabuTenure(courseList, neighborhoodList)

    def addTabuMove(self, courseId, period, roomId):
        move = Move(period, roomId)
        self.tabuList[courseId].append(move)

    """Function to count coeficient for tabu tenure (number of conflicting courses / total number of courses)"""
    def coeficientTabuTenure(self, courseList, neighborhoodList):
        totalNumberOfCourses = len(courseList)
        parameter = {x.id : [] for x in courseList}

        map(lambda x : parameter[x].append(float(len(neighborhoodList[x])) / float(totalNumberOfCourses)), neighborhoodList)
        return parameter

    """Tabu tenure of courseId is tuned adaptively according to the current solution quality f and moving frequency"""
    def tabuTenure(self, courseId, partialTimetable, data):
        """Moving frequency of lectures of courseId"""
        movingFreqCourse = len(self.tabuList[courseId])
        f = softConstraints.totalSoftConstraintsForTimetable(partialTimetable, data)
        tt =  f + self.parameter[courseId][0] * movingFreqCourse
        return tt




def initialSolution(timetable, data):

    pass



"""Matching algorithm to make room allocations (number of courses in slot <= number of rooms)"""
"""Return timetable[slot] with assigned rooms to courses"""
"""Match rooms to courses starting from courses with the biggest number of students, match the biggest available room"""
def matchingRoomAllocations(timetable, slot, data, sortedRoomIdList):
    studentsForCourse= {x.courseId: data.getCourse(x.courseId).studentsNum for x in timetable[slot]}
    sortedStudentsForCourse = sorted(studentsForCourse.iteritems(), key=operator.itemgetter(1), reverse=True)
    for x in timetable[slot]:
        indexOfRoom = map(operator.itemgetter(0), sortedStudentsForCourse).index(x.courseId)
        x.roomId = sortedRoomIdList[indexOfRoom].id

    return timetable[slot]













