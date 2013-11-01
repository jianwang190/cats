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

"""Cell to keep data about course for BasicNeighborhood structure"""
class CellBasicNeighborhood(object):
    """"Index - index on list in timeTable[period]"""
    def __init__(self, courseId = [], period = [], index = []):
        self.courseId = courseId
        self.period = period
        self.index = index

"""Structure to which contains all possible swaps between courses"""
class BasicNeighborhood(object):
    def __init__(self):
        self.basicList = []

    """Add possible swap between courses"""
    def addCell(self, cellFirst, cellSecond):
        self.basicList.append((cellFirst, cellSecond))

    def getBasicList(self):
        return self.basicList


    """Check is swap between two courses if possible regarding other courses in slot"""
    """if courseIdSecond can be assigned to slot"""
    def checkSimpleSwapMove(self, timetable, neighbourhoodList, courseIdFirst, courseIdSecond, slot):
        curCourseSet = filter(lambda z: z != set([]), map(lambda x : neighbourhoodList[courseIdSecond] & neighbourhoodList[x.courseId], \
                           filter(lambda y : y.courseId != courseIdFirst, timetable[slot])))
        return False if len(curCourseSet) > 0 else True

    """Finds all possible swaps between courses or to empty position, create basicList structure"""
    def simpleSwap(self, timetable, neighborhoodList):
        for i in range(0, len(timetable)):

            for indexFirst in range(0, len(timetable[i])):
                cellFirst = timetable[i][indexFirst]


                for j in range(i, len(timetable)):
                    """Swap two courses"""
                    for indexSecond in range(0, len(timetable[j])):
                        cellSecond = timetable[j][indexSecond]
                        if cellSecond.courseId != cellFirst.courseId:
                            if self.checkSimpleSwapMove(timetable, neighborhoodList, cellSecond.courseId, cellFirst.courseId, j) \
                                    & self.checkSimpleSwapMove(timetable, neighborhoodList, cellFirst.courseId, cellSecond.courseId, i):
                                basicFirst = CellBasicNeighborhood(cellFirst.courseId, i, indexFirst)
                                basicSecond = CellBasicNeighborhood(cellSecond.courseId, j, indexSecond)
                                self.addCell(basicFirst, basicSecond)

                    """Assigned course to slot (to empty position)"""
                    if self.checkSimpleSwapMove(timetable, neighborhoodList, [], cellFirst.courseId, j):
                        basicFirst = CellBasicNeighborhood(cellFirst.courseId, i, indexFirst)
                        basicSecond = CellBasicNeighborhood([], j, [])
                        self.addCell(basicFirst, basicSecond)

            """Empty position change with arbitrary course"""
            if len(timetable[i]) == 0:
                for j in range(i, len(timetable)):
                    for indexSecond in range(0, len(timetable[j])):
                        cellSecond = timetable[j][indexSecond]
                        basicSecond = CellBasicNeighborhood(cellSecond.courseId, i, indexSecond)
                        basicFirst = CellBasicNeighborhood([], i, [])
                        self.addCell(basicFirst, basicSecond)

        print("WYNIKI")
        for x in self.basicList:
            print("PARA")
            print(x[0].courseId, x[0].period, x[0].index)
            print(x[1].courseId, x[1].period, x[1].index)








