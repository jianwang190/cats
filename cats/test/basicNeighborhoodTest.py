
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


    def test_simpeSwap(self):
        assignedList = [(0, 'c0001', 'B'), (0, 'c0014', 'B'), (2, 'c0030', 'B'), (2, 'c0001', 'B')]
        self.t.addDataToTimetable(assignedList)
        basicNeighborHood = BasicNeighborhood(self.data)
        basicNeighborHood.simpleSwap(self.t.timeTable, self.t.neighbourhoodList, 6)
        self.assertEqual(len(basicNeighborHood.getBasicList()), 103)

    def test_simpeSwap2(self):
        path = u"data/TabuSearchDataTests/simpleSwapMove"
        self.t.readLecturesToTimetable(path)
        basicNeighborHood = BasicNeighborhood(self.data)
        basicNeighborHood.simpleSwap(self.t.timeTable, self.t.neighbourhoodList, 6)
        self.assertEqual(len(basicNeighborHood.getPossibleSwapsForCourse('c0001', 0)), 20)
        self.assertEqual(len(basicNeighborHood.getPossibleSwapsForCourse('c0014', 0)), 27)
        self.assertEqual(len(basicNeighborHood.getPossibleSwapsForCourse('c0005', 1)), 26)
        self.assertEqual(len(basicNeighborHood.getPossibleSwapsForCourse('c0016', 5)), 28)
        #for x in basicNeighborHood.getPossibleSwapsForCourse('c0030', 2):
         #   print("PARA")
          #  print(x[0].courseId, x[0].period, x[0].index)
           # print(x[1].courseId, x[1].period, x[1].index)
        self.assertEqual(len(basicNeighborHood.getPossibleSwapsForCourse('c0030', 2)), 31)


    def test_basicList(self):
        initialSolution(self.t, self.data)
        tabuList = TabuList(self.data.getAllCourses(), self.t.neighbourhoodList)
        tabuList.addTabuMove("c0001", 1, "a", 1)
        self.assertTrue(tabuList.isTabuMove("c0001", 1, "a",2, 10))


if __name__=="__main__":
    unittest.main()
