
"""Basic Neighborhood - exchanging the hosting periods and rooms assigned to two lectures of different courses """

"""Cell to keep data about course for BasicNeighborhood structure"""
class CellBasicNeighborhood(object):
    """"Index - index on list in timeTable[period]"""
    def __init__(self, courseId, period, index):
        self.courseId = courseId
        self.period = period
        self.index = index

"""Structure containing all possible swaps between courses"""
class BasicNeighborhood(object):
    def __init__(self):
        self.basicList = []

    def clearBasicList(self):
        self.basicList = []

    """Add possible swap between courses"""
    def addCell(self, cellFirst, cellSecond):

        self.basicList.append((cellFirst, cellSecond))

    """Get list containing possible swaps"""
    def getBasicList(self):
        return self.basicList


    """Check is swap between two courses if possible regarding other courses in slot (neighbourhoodList)"""
    """if courseIdSecond can be assigned to slot"""
    def checkSimpleSwapMove(self, timetable, neighbourhoodList, courseIdFirst, courseIdSecond, slot):
        curCourseSet = filter(lambda z: z != set([]), map(lambda x : neighbourhoodList[courseIdSecond] & neighbourhoodList[x[0]], \
                           filter(lambda y : y[0] != courseIdFirst, timetable[slot])))
        return False if len(curCourseSet) > 0 else True


    def checkIfNotInBasicNeighbourhood(self, courseIdFirst, slotFirst, courseIdSecond, slotSecond):
        """
        Check if swap between courses exists in BasicNeighbourhood structure
        :param courseIdFirst:first course id
        :param slotFirst: slot to which first course id is assigned
        :param courseIdSecond: second course id
        :param slotSecond: slot to which second course id is assigned
        :return:
        """
        for cells in self.basicList:
            if (cells[0].courseId == courseIdFirst and cells[0].period == slotFirst \
                and cells[1].courseId == courseIdSecond and cells[1].period == slotSecond):
                return True
            elif (cells[1].courseId == courseIdFirst and cells[1].period == slotFirst \
                      and cells[0].courseId == courseIdSecond and cells[0].period == slotSecond):
                return True
        return False

    def simpleSwap(self, timetable, neighborhoodList, numberOfRooms):

        """
        Finds all possible swaps between courses or to empty position, create basicList structure
        :param timetable:
        :param neighborhoodList:
        :param numberOfRooms:
        """
        SIZE = len(timetable)

        for i in range(0, SIZE):

            for indexFirst in range(0, len(timetable[i])):
                cellFirst = timetable[i][indexFirst]

                for j in range(0, SIZE):
                    """Swap two courses"""
                    if j != i:
                        for indexSecond in range(0, len(timetable[j])):
                            cellSecond = timetable[j][indexSecond]
                            if cellSecond[0] != cellFirst[0]:
                                if self.checkSimpleSwapMove(timetable, neighborhoodList, cellSecond[0], cellFirst[0], j) \
                                        & self.checkSimpleSwapMove(timetable, neighborhoodList, cellFirst[0], cellSecond[0], i):

                                    if self.checkIfNotInBasicNeighbourhood(cellFirst[0], i, cellSecond[0], j) is False:
                                        basicFirst = CellBasicNeighborhood(cellFirst[0], i, indexFirst)
                                        basicSecond = CellBasicNeighborhood(cellSecond[0], j, indexSecond)
                                        self.addCell(basicFirst, basicSecond)

                        """Swap (assign) course with empty position"""
                        if self.checkSimpleSwapMove(timetable, neighborhoodList, [], cellFirst[0], j) and len(timetable[j]) < numberOfRooms:
                            if self.checkIfNotInBasicNeighbourhood(cellFirst[0], i, [], j) is False:
                                basicFirst = CellBasicNeighborhood(cellFirst[0], i, indexFirst)
                                basicSecond = CellBasicNeighborhood([], j, [])
                                self.addCell(basicFirst, basicSecond)

    """Get all possible swaps for courseId - helper function for tests"""
    def getPossibleSwapsForCourse(self, courseId, slot):
        listForCourse = []
        for x in self.basicList:
            if((x[0].courseId == courseId and x[0].period == slot) or (x[1].courseId == courseId and x[1].period == slot)):
                listForCourse.append(x)
        return listForCourse