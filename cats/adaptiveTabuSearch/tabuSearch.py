import operator
from cats.adaptiveTabuSearch.advancedNeighborhood import AdvancedNeighborhood
from cats.adaptiveTabuSearch.tabuLists import TabuList, AdvancedTabuList
from cats.adaptiveTabuSearch import softConstraints2
from cats.adaptiveTabuSearch.basicNeighborhood import BasicNeighborhood
import time
from cats.utils.timetable import TimeTable

"""Tabu search algorithm"""
"""Period related costs - sum(minimumWorkingDays, curriculumCompactness)"""
"""Room related costs - sum(roomCapacity, roomStability)"""

PERIOD_RELATED_COST_TAU = 2
DEPTH_OF_TABU_SEARCH = 10


def doSimpleSwap(timetable, (swap1, swap2)):
    newTimetable = {x: timetable[x][:] for x in timetable.keys()}
    if(swap2.index == []):
        newTimetable[swap2.period].append(newTimetable[swap1.period][swap1.index])
        del newTimetable[swap1.period][swap1.index]
    else:
        newTimetable[swap1.period][swap1.index], newTimetable[swap2.period][swap2.index] = \
            newTimetable[swap2.period][swap2.index], newTimetable[swap1.period][swap1.index]
    return newTimetable

def tabuSimpleNeighborhood(timetable, data, theta):

    initialSolution = timetable.copy()

    tabuList = TabuList(data.getAllCourses(), initialSolution.neighbourhoodList)
    b = BasicNeighborhood()
    currentBestSolution = initialSolution.getTimeTable()
    currentBestQuality = softConstraints2.totalSoftConstraintsForTimetable(initialSolution.getTimeTable(), data)
    for i in xrange(theta):
        b.clearBasicList()

        b.simpleSwap(initialSolution.getTimeTable(), initialSolution.neighbourhoodList, len(data.getAllRooms()))
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

        candidates = map(lambda x: (x, doSimpleSwap(initialSolution.getTimeTable(), x)), neighborhood)
        initialQuality = softConstraints2.totalSoftConstraintsForTimetable(initialSolution.getTimeTable(), data)
        print initialQuality, len(neighborhood)

        candidatesAfterPeriods = map(lambda x:  (x,  softConstraints2.totalSoftConstraintsForTimetable(x[1], data)), candidates)

        bestSwap = sorted(candidatesAfterPeriods, key=lambda x: x[1])[0]
        (first, second) = bestSwap[0][0]

        if first.courseId!=[]:
            tabuList.addTabuMove(first.courseId, first.period, initialSolution.getTimeTable()[first.period][first.index][1], i)
        if second.courseId!=[]:
            tabuList.addTabuMove(second.courseId, second.period, initialSolution.getTimeTable()[second.period][second.index][1], i)

        initialSolution.timeTable = bestSwap[0][1]
        if bestSwap[1]<currentBestQuality:
            currentBestQuality, currentBestSolution = bestSwap[1], bestSwap[0][1]

    initialSolution.timeTable = currentBestSolution


    sortedRoomIdList = sorted(data.getAllRooms(), key=lambda room: room.capacity, reverse=True)
    for x in currentBestSolution.keys():
        currentBestSolution[x] = matchingRoomAllocations(currentBestSolution, x, data, sortedRoomIdList)

    print "KARA ", softConstraints2.totalSoftConstraintsForTimetable(currentBestSolution, data)

    initialSolution.timeTable = currentBestSolution
    return initialSolution



def doKempeSwap(((period1, period2), swap), timetable):
    newTimetable = {x: timetable[x][:] for x in timetable.keys()}
    newTimetable[period1] = [x for x in swap["newPeriods"][0]]
    newTimetable[period2] = [x for x in swap["newPeriods"][1]]
    return newTimetable

def tabuAdvancedNeighborhood(timetable, data, theta):

    initialSolution = timetable.copy()

    tabuList = AdvancedTabuList(data.getAllCourses(), initialSolution.neighbourhoodList)
    b= AdvancedNeighborhood()
    currentBestSolution = initialSolution.getTimeTable()
    currentBestQuality = softConstraints2.totalSoftConstraintsForTimetable(initialSolution.getTimeTable(), data)


    for i in xrange(theta):

        tabuTenure = {x.id : tabuList.tabuTenure(x.id, initialSolution.getTimeTable(), data) for x in data.getAllCourses()}

        neighborhood = filter(lambda x: \
            any(map(lambda y: tabuList.isTabuMove(y[0], x[1]["moves"][0][0], i, tabuTenure[y[0]]), x[1]["moves"][0][1]))==False and \
            any(map(lambda y: tabuList.isTabuMove(y[0], x[1]["moves"][1][0], i, tabuTenure[y[0]]), x[1]["moves"][0][1]))==False,
            b.exploreNeighborhood(initialSolution, data))

        candidates = map(lambda x: doKempeSwap(x, initialSolution.getTimeTable()), neighborhood)
        candidates = sorted(map(lambda x: (x, softConstraints2.totalSoftConstraintsForTimetable2(x, data)), candidates), key=lambda x: x[1])

        bestCandidate, bestCandidateQuality = candidates[0]

        initialSolution.timeTable = {x: bestCandidate[x][:] for x in bestCandidate.keys()}
        #print bestCandidateQuality, len(neighborhood), softConstraints2.totalSoftConstraintsForTimetable2(initialSolution.getTimeTable(), data), \
        #    softConstraints2.totalSoftConstraintsForTimetable(bestCandidate, data)

        if bestCandidateQuality<currentBestQuality:
            currentBestSolution = {x: bestCandidate[x][:] for x in bestCandidate.keys()}
            currentBestQuality = bestCandidateQuality
            print softConstraints2.totalSoftConstraintsForTimetable(currentBestSolution, data)


    sortedRoomIdList = sorted(data.getAllRooms(), key=lambda room: room.capacity, reverse=True)
    for x in currentBestSolution.keys():
        currentBestSolution[x] = matchingRoomAllocations(currentBestSolution, x, data, sortedRoomIdList)




    initialSolution.timeTable = {x: currentBestSolution[x][:] for x in currentBestSolution.keys()}




    return initialSolution



def tabuSearch(initialSolution, data, theta):
    improved = True
    bestSolution= initialSolution.copy()
    bestQuality = softConstraints2.totalSoftConstraintsForTimetable(bestSolution.getTimeTable(), data)
    while improved:
        simpleNeighborhood = tabuSimpleNeighborhood(initialSolution.copy(), data, theta)

        advancedNeighborhood = tabuAdvancedNeighborhood(simpleNeighborhood.copy(), data, theta/3)

        if softConstraints2.totalSoftConstraintsForTimetable(advancedNeighborhood.getTimeTable(), data) \
                < bestQuality:
            improved = True
            bestSolution = advancedNeighborhood.copy()
            initialSolution = advancedNeighborhood.copy()

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

    #sortedRoomIdList.sort(key= lambda x: x.capacity, reverse=True)
    studentsForCourse= {x[0]: data.getCourse(x[0]).studentsNum for x in timetable[slot]}
    sortedStudentsForCourse = sorted(studentsForCourse.iteritems(), key=operator.itemgetter(1), reverse=True)
    size = len(timetable[slot])
    for i in range(0, size):
        indexOfRoom = map(operator.itemgetter(0), sortedStudentsForCourse).index(timetable[slot][i][0])
        # modify room Id
        tuple = timetable[slot][i]
        timetable[slot][i] = (tuple[0], sortedRoomIdList[indexOfRoom].id)

    return timetable[slot]













