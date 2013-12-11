import unittest
from cats.adaptiveTabuSearch import heuristics
from cats.readers.competitionReader import CompetitionDictReader
from cats.utils.timetable import TimeTableFactory


class heuristicTest(unittest.TestCase):
    def setUp(self):
        c = CompetitionDictReader()
        self.data = c.readInstance(1)
        self.t = TimeTableFactory.getTimeTable(self.data)
        


    """TODO: write unittests"""
    def testHR1(self):
    	self.assertTrue( \
            heuristics.getNextCourse(self.t, self.data)!=None)

    """TODO: write unittests"""
    def testUnfinishedCourses(self):
        assignedList = [(3, 'c0004', 'B'), (4, 'c0004', 'B'), (5, 'c0004', 'B')]
        self.t.addDataToTimetable(assignedList)
        self.assertEquals(self.t.unavailableUnfinishedCoursesLectureNum(3, 'c0024', self.data), 25)

    def testFeasibleInsertion(self):
        heuristics.feasibleInsertion(self.t, 'c0004', self.data)

    def testInitialSolution(self):
        heuristics.initialSolution(self.t, self.data)
        # self.t.saveResultsToFile("/home/filip/Inzynierka/cats/kumple.txt")
