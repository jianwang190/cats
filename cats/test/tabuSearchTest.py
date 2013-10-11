import unittest
from cats.tabuSearch.tabuSearch import TimeTable
from cats.readers.competitionReader import CompetitionReader
from random import randint
from cats.utils.data import Data

class TabuSearchTest(unittest.TestCase):
    def setUp(self):
        self.c = CompetitionReader()
        self.data = self.c.readInstance(1)
        self.t = TimeTable(self.data.daysNum, self.data.periods_per_day)

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
        self.t.timeTable[0] = ['c0001', 'B']
        self.t.timeTable[1] = ['c0002', 'B']
        self.t.timeTable[2] = ['c0001', 'B']
        self.t.timeTable[24] = ['c0001', 'B']
        counter = self.t.availableNumberOfPeriods(self.data.constraints, 'c0002')
        self.assertEqual(counter, 26)
        counter = self.t.availableNumberOfPeriods(self.data.constraints, 'c0001')
        self.assertEqual(counter, 21)
if __name__=="__main__":
    unittest.main()
