import unittest
from cats.tabuSearch import heuristics
from cats.readers.competitionReader import CompetitionDictReader
from cats.utils.timetable import TimeTableFactory, CellOfTimeTable


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
        self.assertTrue(1==1)



