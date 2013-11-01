import unittest
from cats.utils.timetable import TimeTable, CellOfTimeTable, TimeTableFactory
from cats.readers.competitionReader import CompetitionDictReader
from cats.adaptiveTabuSearch import tabuSearch, softConstraints

class MaximumMatchingTest(unittest.TestCase):
    def setUp(self):
        self.c = CompetitionDictReader()
        self.data = self.c.readInstance(1)
        self.t = TimeTableFactory.getTimeTable(self.data)
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


    def test_checkSimpleSwapMove2(self):
        assignedList = [(0, 'c0001', 'B'), (0, 'c0014', 'B'), (2, 'c0030', 'B'), (2, 'c0001', 'B')]
        self.t.addDataToTimetable(assignedList)
        basicNeighborHood = tabuSearch.BasicNeighborhood()

        """Check if possible to change course 'c0001' with 'c0030' (if 'c0030' can be assigned to slot == 0)"""
        self.assertTrue(basicNeighborHood.checkSimpleSwapMove(self.t.timeTable, self.t.neighbourhoodList, 'c0001', 'c0030', 0) is True)
        """Check if possible to change course 'c0001' with 'c0030' (if 'c0001' can be assigned to slot == 2)"""
        self.assertTrue(basicNeighborHood.checkSimpleSwapMove(self.t.timeTable, self.t.neighbourhoodList, 'c0030', 'c0001', 2) is False)



    def test_simpeSwap(self):
        assignedList = [(0, 'c0001', 'B'), (0, 'c0014', 'B'), (2, 'c0030', 'B'), (2, 'c0001', 'B')]
        self.t.addDataToTimetable(assignedList)
        basicNeighborHood = tabuSearch.BasicNeighborhood()
        basicNeighborHood.simpleSwap(self.t.timeTable, self.t.neighbourhoodList)
        print("LISTA")
        print(basicNeighborHood.basicList)
        #self.assertEqual(len(basicNeighborHood.getBasicList()), 113)


if __name__=="__main__":
    unittest.main()



