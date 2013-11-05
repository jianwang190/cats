import unittest
from cats.utils.timetable import TimeTable, CellOfTimeTable, TimeTableFactory
from cats.readers.competitionReader import CompetitionDictReader
from cats.adaptiveTabuSearch import tabuSearch, softConstraints
from cats.adaptiveTabuSearch.heuristics import initialSolution
import time

class MaximumMatchingTest(unittest.TestCase):
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
        listOfAssignedRooms = [x.roomId for x in self.t.timeTable[slot]]
        self.assertEqual(listOfAssignedRooms, ['B', 'S', 'C', 'G', 'F'])
        penalty = sum(map(lambda x: softConstraints.softConstraintsPenalty(self.t.getTimeTable(), self.data, x)['penaltyRoomCapacity'], coursesId))
        self.assertEqual(penalty, 340)

        slot = 1
        self.t.timeTable[slot] = tabuSearch.matchingRoomAllocations(self.t.getTimeTable(), slot, self.data, self.sortedRoomIdList)
        listOfAssignedRooms = [x.roomId for x in self.t.timeTable[slot]]
        self.assertEqual(listOfAssignedRooms, ['G', 'S', 'E', 'B', 'C', 'F'])
        penalty = sum(map(lambda x: softConstraints.softConstraintsPenalty(self.t.getTimeTable(), self.data, x)['penaltyRoomCapacity'], coursesId))
        self.assertEqual(penalty, 305)

    def test_coeficientTabuTenure(self):
        tabu = tabuSearch.TabuList(self.data.getAllCourses(), self.t.neighbourhoodList)
        courseIds = ['c0070', 'c0001', 'c0004']
        result = sum(map(lambda y: tabu.parameter[y][0], filter(lambda x: x in courseIds, tabu.parameter)))
        self.assertTrue(format(result, '.2f'), 0.43)

    #def test_tabuTenure(self):
    #    tabu = tabuSearch.TabuList(self.data.getAllCourses(), self.t.neighbourhoodList)
    #    assignedList = [(0, 'c0001', 'E'), (1, 'c0001', 'B'), (4, 'c0001', 'C'), (7, 'c0002', 'G'), (9, 'c0072', 'E')]
    #    self.t.addDataToTimetable(assignedList)
    #    tabu.addTabuMove('c0001', 10, 'E')
    #    tabu.addTabuMove('c0001', 12, 'E')
    #    result = tabu.tabuTenure('c0001', self.t.getTimeTable(), self.data)
    #    self.assertEqual(result, 244.4)

    #def testATS(self):
    #    for i in range(1,22):
    #        self.data = self.c.readInstance(i)
    #        self.t = TimeTableFactory.getTimeTable(self.data)
    #        start = time.time()
    #        initialSolution(self.t, self.data)
    #        print "[%d] ATS INITIAL PHASE" % i, time.time() - start
    #        self.assertSequenceEqual(self.data.getUnfinishedCourses(), [])

if __name__=="__main__":
    unittest.main()



