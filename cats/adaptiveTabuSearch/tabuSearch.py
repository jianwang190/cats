import operator
"""Tabu search algorithm"""
"""Period related costs - sum(minimumWorkingDays, curriculumCompactness)"""
"""Room related costs - sum(roomCapacity, roomStability)"""

PERIOD_RELATED_COST_TAU = 2
DEPTH_OF_TABU_SEARCH = 10

def initialSolution(timetable, data):

    pass


def simpleSwap(timetable):
    pass

"""Single and double kempe swap"""
def kempeSwap(timetable):
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

"""page 9 description"""
def tabuTenure(courseId):
    pass

"""Moving frequency of lectures of courseId"""
def movingFrequency(courseId):
    pass

"""Function to count coeficient for tabu tenure (number of conflicting courses / total number of courses)"""
def coeficientTabuTenure():
    pass








