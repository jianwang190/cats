import unittest
import os
from cats.tabuSearch.tabuSearch import TimeTable, CellOfTimeTable
from cats.readers.competitionReader import CompetitionReader
from random import randint
from cats.utils.data import Data

class TabuSearchTest(unittest.TestCase):
    def setUp(self):
        self.c = CompetitionReader()
        self.data = self.c.readInstance(1)
        self.t = TimeTable(self.data.daysNum, self.data.periods_per_day)
	self.t.neighbourhoodList = self.t.createNeighbourhoodList(self.data.curricula, self.data.courses)
    def test_initial(self):
        self.assertEquals(len(self.t.getTimeTable()), 30)
        day = randint(0, self.data.daysNum - 1)
        day_period = randint(0, self.data.periods_per_day - 1)
    	self.assertEquals(self.t.getValueSlot(day, day_period), [])

    def test_getKeyConstraintsOfCourse(self):
        keysConstraintsOfCourse = self.t.getKeyConstraintsOfCourse(self.data.constraints, 'c0001')
        self.assertEqual(keysConstraintsOfCourse, [24, 25, 26, 27, 28, 29])

    def test_availableNumberOfPeriods1(self):
        counter = self.t.availableNumberOfPeriods(self.data.constraints, 'c0001')
        self.assertEqual(counter, 24)
        counter = self.t.availableNumberOfPeriods(self.data.constraints, 'c0002')
        self.assertEqual(counter, 30)

    def test_availableNumberOfPeriods2(self):
        self.t.timeTable[0].append(CellOfTimeTable('c0001', 'B'))
        self.t.timeTable[1].append(CellOfTimeTable('c0002', 'B'))
        self.t.timeTable[2].append(CellOfTimeTable('c0001', 'B'))
        self.t.timeTable[24].append(CellOfTimeTable('c0001', 'B'))
        counter = self.t.availableNumberOfPeriods(self.data.constraints, 'c0001')
        self.assertEqual(counter, 21)
        counter = self.t.availableNumberOfPeriods(self.data.constraints, 'c0002')
        self.assertEqual(counter, 26)

    def test_availableNumberOfPeriods3(self):
        self.t.timeTable[0].append(CellOfTimeTable('c0001', 'B'))
        self.t.timeTable[1].append(CellOfTimeTable('c0002', 'B'))
        self.t.timeTable[1].append(CellOfTimeTable('c0014', 'C'))
        self.t.timeTable[3].append(CellOfTimeTable('c0014', 'C'))
        self.t.timeTable[2].append(CellOfTimeTable('c0004', 'C'))
        self.t.timeTable[24].append(CellOfTimeTable('c0001', 'B'))
        counter = self.t.availableNumberOfPeriods(self.data.constraints, 'c0001')
        self.assertEqual(counter, 21)
        counter = self.t.availableNumberOfPeriods(self.data.constraints, 'c0002')
        self.assertEqual(counter, 26)
        counter = self.t.availableNumberOfPeriods(self.data.constraints, 'c0014')
        self.assertEqual(counter, 28)
        counter = self.t.availableNumberOfPeriods(self.data.constraints, 'c0071')
        self.assertEqual(counter, 15)

    def test_createNeighbourhoodList(self):
        neighbourhoodList = self.t.createNeighbourhoodList(self.data.curricula, self.data.courses)
        path = u"data/TabuSearchDataTests/neighbourhoodCourses"
        f = open(path, "r")
        self.assertEqual(str(neighbourhoodList), f.readline().strip())
if __name__=="__main__":
    unittest.main()
