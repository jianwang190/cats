import operator
from cats.adaptiveTabuSearch import softConstraints2
from cats.adaptiveTabuSearch.basicNeighborhood import BasicNeighborhood

"""Tabu search algorithm"""
"""Period related costs - sum(minimumWorkingDays, curriculumCompactness)"""
"""Room related costs - sum(roomCapacity, roomStability)"""

PERIOD_RELATED_COST_TAU = 2
DEPTH_OF_TABU_SEARCH = 10
#

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

    def __contains__(self, (course, period, room)):
        return any(map(lambda x: x.period==period and x.room==room, self.tabuList[course]))


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




class AdvancedTabuList(object):
    def __init__(self):
        pass

    def addTabuMoves(self, tabuListMoves):
        pass



def doSimpleSwap(timetable, (swap1, swap2)):
    newTimetable = timetable.getTimeTable().copy()
    #TODO: swap2.index == [] or swap.1.index == []
    if(swap2.index == []):
        print swap1.period, newTimetable[swap1.period]
        assert(len(newTimetable[swap1.period])> swap1.index)
        #newTimetable[swap2.period].append(newTimetable[swap1.period][swap1.index])
        #del newTimetable[swap1.period][swap1.index]
    else:
        newTimetable[swap1.period][swap1.index], newTimetable[swap2.period][swap2.index] = \
            newTimetable[swap2.period][swap2.index], newTimetable[swap1.period][swap1.index]
    return newTimetable

def tabuSimpleNeighborhood(initialSolution, data, theta):
    tabuList = TabuList(data.getAllCourses(), initialSolution.neighbourhoodList)
    b = BasicNeighborhood()
    b.clearBasicList()
    for i in xrange(theta):
        b.simpleSwap(initialSolution.getTimeTable(), initialSolution.neighbourhoodList, len(data.getAllCourses()))
        neighborhood = filter(lambda swap: \
                (swap[0].courseId, swap[0].period, initialSolution.getTimeTable()[swap[0].period][swap[0].index][1]) not in tabuList\
                and (swap[1].courseId==[] or\
                (swap[1].courseId, swap[1].period, initialSolution.getTimeTable()[swap[1].period][swap[1].index][1]) not in tabuList), \
                b.getBasicList())

        candidates = map(lambda x: doSimpleSwap(initialSolution, x), neighborhood)
        initialQuality = softConstraints2.totalSoftConstraintsForTimetable(initialSolution.getTimeTable(), data)
        candidatesAfterPeriods = filter(lambda x: x[1]-initialQuality>0, \
                map(lambda x:  (x, softConstraints2.totalSoftConstraintsForTimetable(initialSolution.getTimeTable(), data)), candidates))
        print initialQuality
        print candidatesAfterPeriods






def tabuAdvancedNeighborhood(initialSolution, theta):
    return initialSolution



def tabuSearch(initialSolution, data, theta):
    improved = True
    bestSolution = initialSolution
    while improved:
        simpleNeighborhood = tabuSimpleNeighborhood(initialSolution, theta)
        advancedNeighborhood = tabuAdvancedNeighborhood(simpleNeighborhood, theta/3.0)
        if softConstraints2.totalSoftConstraintsForTimetable(advancedNeighborhood, data) < softConstraints2.totalSoftConstraintsForTimetable(bestSolution, data):
            improved = True
            bestSolution = advancedNeighborhood
            initialSolution = advancedNeighborhood
        else:
            improved = False

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
    studentsForCourse= {x[0]: data.getCourse(x[0]).studentsNum for x in timetable[slot]}
    sortedStudentsForCourse = sorted(studentsForCourse.iteritems(), key=operator.itemgetter(1), reverse=True)
    size = len(timetable[slot])
    for i in range(0, size):
        indexOfRoom = map(operator.itemgetter(0), sortedStudentsForCourse).index(timetable[slot][i][0])
        # modify room Id
        tuple = timetable[slot][i]
        timetable[slot][i] = (tuple[0], sortedRoomIdList[indexOfRoom].id)

    return timetable[slot]













