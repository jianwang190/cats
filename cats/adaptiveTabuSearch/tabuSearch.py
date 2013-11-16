import operator
from cats.adaptiveTabuSearch import softConstraints2
from cats.adaptiveTabuSearch.basicNeighborhood import BasicNeighborhood
import time
"""Tabu search algorithm"""
"""Period related costs - sum(minimumWorkingDays, curriculumCompactness)"""
"""Room related costs - sum(roomCapacity, roomStability)"""

PERIOD_RELATED_COST_TAU = 2
DEPTH_OF_TABU_SEARCH = 10
#

class Move(object):
    def __init__(self, period, roomId, iteration):
        self.period = period
        self.room = roomId
        self.iteration = iteration


# separate object of TabuList class should be created for N1 and N2
class TabuList(object):
    """"Contain tabu moves in tabuList"""
    def __init__(self, courseList, neighborhoodList):
        self.tabuList = {x.id : [] for x in courseList}
        self.parameter = self.coefficientTabuTenure(courseList, neighborhoodList)


    def addTabuMove(self, courseId, period, roomId, iteration):
        move = Move(period, roomId, iteration)
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

    def isTabuMove(self, courseId, period, roomId, currentIteration, tt):
        #print [(x.period,x.room,  x.iteration) for x in self.tabuList[courseId]]
        #print filter(lambda x: x.period==period and x.room==roomId, self.tabuList[courseId])
        return len( \
            filter(lambda x: x.period==period and x.room==roomId and x.iteration+tt>=currentIteration, self.tabuList[courseId]))>0






class AdvancedTabuList(object):
    def __init__(self):
        pass

    def addTabuMoves(self, tabuListMoves):
        pass



def doSimpleSwap(timetable, (swap1, swap2)):

    newTimetable = {x: timetable.getTimeTable()[x][:] for x in timetable.getTimeTable().keys()}
    if(swap2.index == []):
        newTimetable[swap2.period].append(newTimetable[swap1.period][swap1.index])
        del newTimetable[swap1.period][swap1.index]
    else:
        newTimetable[swap1.period][swap1.index], newTimetable[swap2.period][swap2.index] = \
            newTimetable[swap2.period][swap2.index], newTimetable[swap1.period][swap1.index]
    return newTimetable

def tabuSimpleNeighborhood(initialSolution, data, theta):
    tabuList = TabuList(data.getAllCourses(), initialSolution.neighbourhoodList)
    b = BasicNeighborhood()
    currentBestSolution = initialSolution.getTimeTable()
    currentBestQuality = softConstraints2.totalSoftConstraintsForTimetable(initialSolution.getTimeTable(), data)
    for i in xrange(theta):
        b.clearBasicList()

        b.simpleSwap(initialSolution.getTimeTable(), initialSolution.neighbourhoodList, len(data.getAllCourses()))
        tabuTenure = {x.id : tabuList.tabuTenure(x.id, initialSolution.getTimeTable(), data) for x in data.getAllCourses()}

        neighborhood = filter(lambda swap: \
            (swap[0].courseId==[] or
                tabuList.isTabuMove(\
                    swap[0].courseId, \
                    swap[0].period, \
                    initialSolution.getTimeTable()[swap[0].period][swap[0].index][1], \
                    i, \
                    tabuTenure[swap[0].courseId]) == False)
                and (swap[1].courseId==[] or \
                tabuList.isTabuMove( \
                    swap[1].courseId, \
                    swap[1].period, \
                    initialSolution.getTimeTable()[swap[1].period][swap[1].index][1],
                    i,\
                    tabuTenure[swap[1].courseId]) == False), \
                b.getBasicList())

        if len(neighborhood)==0:
            break

        candidates = map(lambda x: (x, doSimpleSwap(initialSolution, x)), neighborhood)
        initialQuality = softConstraints2.totalSoftConstraintsForTimetable(initialSolution.getTimeTable(), data)
        print initialQuality, len(neighborhood)

        candidatesAfterPeriods = map(lambda x:  (x,  softConstraints2.totalSoftConstraintsForTimetable(x[1], data)), candidates)

        bestSwap = sorted(candidatesAfterPeriods, key=lambda x: x[1])[0]
        (first, second) = bestSwap[0][0]


        if first.courseId!=[]:
            tabuList.addTabuMove(first.courseId, first.period, initialSolution.getTimeTable()[first.period][first.index][1], i)
        if second.courseId!=[]:
            tabuList.addTabuMove(second.courseId, second.period, initialSolution.getTimeTable()[second.period][second.index][1], i)

        print "FIRST:  ",first.courseId, first.period
        print "SECOND: ", second.courseId, second.period
        for i in tabuList.tabuList.keys():
            print i, tabuTenure[i],[(x.period, x.room, x.iteration) for x in tabuList.tabuList[i]]

        initialSolution.timeTable = bestSwap[0][1]
        if bestSwap[1]<currentBestQuality:
            currentBestQuality, currentBestSolution = bestSwap[1], bestSwap[0][1]
    initialSolution.timeTable = currentBestSolution
    print "CURRENT BEST: ", currentBestQuality
    print "CURRENT BEST: ", currentBestSolution

    return initialSolution










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













