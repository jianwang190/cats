
import unittest
from cats.adaptiveTabuSearch.heuristics import initialSolution
from cats.adaptiveTabuSearch.tabuSearch import TabuList
from cats.utils.timetable import TimeTableFactory
from cats.readers.competitionReader import CompetitionDictReader
from cats.adaptiveTabuSearch.basicNeighborhood import BasicNeighborhood

class BasicNeighborhoodTest(unittest.TestCase):
    def setUp(self):
        self.c = CompetitionDictReader()
        self.data = self.c.readInstance(1)
        self.t = TimeTableFactory.getTimeTable(self.data)

    def test_checkSimpleSwapMove2(self):
        assignedList = [(0, 'c0001', 'B'), (0, 'c0014', 'B'), (2, 'c0030', 'B'), (2, 'c0001', 'B')]
        self.t.addDataToTimetable(assignedList)
        basicNeighborHood = BasicNeighborhood(self.data)

        """Check if possible to change course 'c0001' with 'c0030' (if 'c0030' can be assigned to slot == 0)"""
        self.assertTrue(basicNeighborHood.checkSimpleSwapMove(self.t.timeTable, self.t.neighbourhoodList, 'c0001', 'c0030', 0) is True)
        """Check if possible to change course 'c0001' with 'c0030' (if 'c0001' can be assigned to slot == 2)"""
        self.assertTrue(basicNeighborHood.checkSimpleSwapMove(self.t.timeTable, self.t.neighbourhoodList, 'c0030', 'c0001', 2) is False)



    def test_simpeSwap(self):
        assignedList = [(0, 'c0001', 'B'), (0, 'c0014', 'B'), (2, 'c0030', 'B'), (2, 'c0001', 'B')]
        self.t.addDataToTimetable(assignedList)
        basicNeighborHood = BasicNeighborhood(self.data)
        basicNeighborHood.simpleSwap(self.t.timeTable, self.t.neighbourhoodList, 6)
        self.assertEqual(len(basicNeighborHood.getBasicList()), 115)

    def test_simpeSwap2(self):
        path = u"data/TabuSearchDataTests/simpleSwapMove"
        self.t.readLecturesToTimetable(path)
        basicNeighborHood = BasicNeighborhood(self.data)
        basicNeighborHood.simpleSwap(self.t.timeTable, self.t.neighbourhoodList, 6)
        self.assertEqual(len(basicNeighborHood.getPossibleSwapsForCourse('c0001', 0)), 28)
        self.assertEqual(len(basicNeighborHood.getPossibleSwapsForCourse('c0014', 0)), 30)
        self.assertEqual(len(basicNeighborHood.getPossibleSwapsForCourse('c0005', 1)), 28)
        self.assertEqual(len(basicNeighborHood.getPossibleSwapsForCourse('c0016', 5)), 31)
        #for x in basicNeighborHood.getPossibleSwapsForCourse('c0030', 2):
         #   print("PARA")
          #  print(x[0].courseId, x[0].period, x[0].index)
           # print(x[1].courseId, x[1].period, x[1].index)
        self.assertEqual(len(basicNeighborHood.getPossibleSwapsForCourse('c0030', 2)), 32)


    def test_basicList(self):
        initialSolution(self.t, self.data)
        tabuList = TabuList(self.data.getAllCourses(), self.t.neighbourhoodList)
        tabuList.addTabuMove("c0001", 1, "a", 1)
        self.assertTrue(tabuList.isTabuMove("c0001", 1, "a",2, 10))


if __name__=="__main__":
    unittest.main()
