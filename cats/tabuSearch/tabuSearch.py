from cats.utils.timetable import TimeTable, CellOfTimeTable, TimeTableFactory

class TabuSearch(object):

    def findMin(self, rightNodes, leftNodes, courseId):
        minSize = 1000000000
        roomId = 0
        for x in leftNodes[courseId]:
            length = len(rightNodes[x])
            if (length  < minSize):
                minSize = length
                roomId = x
        return roomId

    """leftNodes: courses : rooms, rightNodes rooms : courses"""
    def createLeftRightLists(self, roomIdsListForCourses, courseIdsListForSlot):

        totalEdgeNumber = 0
        leftNodes = dict()
        rightNodes = dict()

        for c in courseIdsListForSlot:
            leftNodes[c.courseId] = roomIdsListForCourses.get(c.courseId)
            totalEdgeNumber += len(leftNodes[c.courseId])

        for c in leftNodes:
            for r in leftNodes[c]:
                rightNodes.setdefault(r, []).append(c)

        return {'leftNodes' : leftNodes, 'rightNodes' : rightNodes, 'totalEdgeNumber' : totalEdgeNumber}

    """Delete all edges which are incident with courseId and roomId"""
    def deleteEdges(self, leftNodes, rightNodes, courseId, roomId):
        for x in leftNodes:
            if(roomId in leftNodes[x]):
                leftNodes[x].remove(roomId)

        for x in rightNodes:
            if(courseId in rightNodes[x]):
                rightNodes[x].remove(courseId)

        leftNodes.pop(courseId)
        rightNodes.pop(roomId)
        totalEdgeNumber = sum([len(leftNodes[x]) for x in leftNodes])
        return {'leftNodes' : leftNodes, 'rightNodes' : rightNodes, 'totalEdgeNumber' : totalEdgeNumber}

    """Algorithm maximum matching rooms for courses in one slot"""
    """TODO: more tests, examples where not exists matching for courses"""
    def maximumMatching(self, roomIdsListForCourses, courseIdsListForSlot):
        result = self.createLeftRightLists(roomIdsListForCourses, courseIdsListForSlot)
        leftNodes = result['leftNodes']
        rightNodes = result['rightNodes']
        totalEdgeNumber = result['totalEdgeNumber']
        matchingList = []
        while (totalEdgeNumber != 0):
            degreeList = ([(x, len(leftNodes[x])) for x in leftNodes])
            courseId , courseVertexDegree= min(degreeList, key = lambda x: x[1])
            if(courseVertexDegree > 1):
                roomId = self.findMin(rightNodes, leftNodes, courseId)
            elif(courseVertexDegree == 1):
                roomId = leftNodes[courseId].pop()

            matchingList.append([courseId, roomId])
            graph = self.deleteEdges(leftNodes, rightNodes, courseId, roomId)
            leftNodes = graph['leftNodes']
            rightNodes = graph['rightNodes']
            totalEdgeNumber = graph['totalEdgeNumber']

        return matchingList




