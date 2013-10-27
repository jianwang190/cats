import unittest
from cats.tabuSearch import heuristics
from cats.readers.competitionReader import CompetitionReader
from cats.utils.timetable import TimeTableFactory, CellOfTimeTable


class heuristicTest(unittest.TestCase):
    def setUp(self):
        c = CompetitionReader()
        self.data = c.readInstance(1)
        self.t = TimeTableFactory.getTimeTable(self.data)

    """TODO: write unittests"""
    def testHR1(self):
    	self.assertTrue( \
            heuristics.getNextCourse(self.t, self.data)!=None)
        print heuristics.getNextCourse(self.t, self.data)




