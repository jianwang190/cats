import unittest
from cats.adaptiveTabuSearch import tabuLists
from cats.adaptiveTabuSearch.advancedNeighborhood import AdvancedNeighborhood
from cats.adaptiveTabuSearch.tabuSearch import tabuAdvancedNeighborhood
from cats.adaptiveTabuSearch.tabuSearch import tabuSimpleNeighborhood
from cats.utils.timetable import TimeTable, TimeTableFactory
from cats.readers.competitionReader import CompetitionDictReader
from cats.adaptiveTabuSearch import tabuSearch, softConstraints2
from cats.adaptiveTabuSearch.heuristics import initialSolution
import time

class TabuSearchTest(unittest.TestCase):
    def setUp(self):
        self.c = CompetitionDictReader()
        self.data = self.c.readInstance(1)
        self.t = TimeTableFactory.getTimeTable(self.data)
        "Create sorted list of rooms (sorted by capacity)"
        self.sortedRoomIdList = sorted(self.data.getAllRooms(), key=lambda room: room.capacity, reverse=True)

    def test_matchRoomAllocation(self):
        path = u"data/TabuSearchDataTests/matchingRooms"
        self.t.readLecturesToTimetable(path)
        slot = 0
        coursesId = ['c0001', 'c0002', 'c0004', 'c0030', 'c0005', 'c0014', 'c0015', 'c0016']
        self.t.timeTable[slot] = tabuSearch.matchingRoomAllocations(self.t.getTimeTable(), slot, self.data, self.sortedRoomIdList)
        listOfAssignedRooms = [x[1] for x in self.t.timeTable[slot]]
        self.assertEqual(listOfAssignedRooms, ['B', 'S', 'C', 'G', 'F'])
        penalty =  softConstraints2.softConstraintsPenalty(self.t.getTimeTable(), self.data)['penaltyRoomCapacity']
        self.assertEqual(penalty, 340)

        slot = 1
        self.t.timeTable[slot] = tabuSearch.matchingRoomAllocations(self.t.getTimeTable(), slot, self.data, self.sortedRoomIdList)
        listOfAssignedRooms = [x[1] for x in self.t.timeTable[slot]]
        self.assertEqual(listOfAssignedRooms, ['G', 'S', 'E', 'B', 'C', 'F'])
        penalty = softConstraints2.softConstraintsPenalty(self.t.getTimeTable(), self.data)['penaltyRoomCapacity']

        self.assertEqual(penalty, 305)

    def test_coeficientTabuTenure(self):
        tabu = tabuSearch.TabuList(self.data.getAllCourses(), self.t.neighbourhoodList)
        courseIds = ['c0070', 'c0001', 'c0004']
        result = sum(map(lambda y: tabu.parameter[y][0], filter(lambda x: x in courseIds, tabu.parameter)))
        self.assertTrue(format(result, '.2f'), 0.43)

    def test_tabuTenure(self):
        tabu = tabuLists.TabuList(self.data.getAllCourses(), self.t.neighbourhoodList)
        assignedList = [(0, 'c0001', 'E'), (1, 'c0001', 'B'), (4, 'c0001', 'C'), (7, 'c0002', 'G'), (9, 'c0072', 'E')]
        self.t.addDataToTimetable(assignedList)
        tabu.addTabuMove('c0001', 10, 'E', 1)
        tabu.addTabuMove('c0001', 12, 'E', 1)
        result = tabu.tabuTenure('c0001', self.t.getTimeTable(), self.data)
        self.assertEqual(result, 733.4)


    def test_advancedList(self):
        initialSolution(self.t, self.data)

        tabuList = tabuLists.AdvancedTabuList(self.data.getAllCourses(), self.t.neighbourhoodList)
        tabuList.addTabuMove("c0068", 0, 1)

        b = AdvancedNeighborhood()
        tabuTenure = {x.id : tabuList.tabuTenure(x.id, self.t.getTimeTable(), self.data) for x in self.data.getAllCourses()}
        for (periods, swaps) in b.exploreNeighborhood(self.t, self.data):
            #print map(lambda y: tabuList.isTabuMove(y[0], x[1]["moves"][0], 1, tabuTenure[y[0]]), x[1]["moves"][0][1])
            #print map(lambda y: tabuList.isTabuMove(y[0], x[1]["moves"][1], 1, tabuTenure[y[0]]), x[1]["moves"][1][1])
            print swaps["moves"]
            print map(lambda y: tabuList.isTabuMove(y[0], swaps["moves"][0][0], 1,tabuTenure[y[0]]), swaps["moves"][0][1])


    #def testSimpleNeighborhood(self):
    #    initialSolution(self.t, self.data)
    #    tabuSimpleNeighborhood(self.t, self.data, 10)
    #
    #def testAdvancedNeighborhood(self):
    #    initialSolution(self.t, self.data)
    #    t = tabuAdvancedNeighborhood(self.t, self.data, 10)
    #    print "QUALITY: ",softConstraints2.softConstraintsPenalty(self.t.getTimeTable(), self.data)
    #
    #def testTabuSearch(self):
    #    initialSolution(self.t, self.data)
    #    t = tabuSearch.tabuSearch(self.t, self.data, 10)




if __name__=="__main__":
    unittest.main()



