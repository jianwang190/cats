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
	self.t.roomsIdListForCourses = self.t.getRoomsIdForCourses(self.data.rooms, self.data.courses)
    def test_initial(self):
        self.assertEquals(len(self.t.getTimeTable()), 30)
        day = randint(0, self.data.daysNum - 1)
        day_period = randint(0, self.data.periods_per_day - 1)
    	self.assertEquals(self.t.getValueSlot(day, day_period), [])

    def test_getKeyConstraintsOfCourse(self):
        keysConstraintsOfCourse = self.t.getKeyConstraintsOfCourse(self.data.constraints, 'c0001')
        self.assertEqual(keysConstraintsOfCourse, [24, 25, 26, 27, 28, 29])

    def test_availableNumberOfPeriods1(self):
        counter = self.t.availableNumberOfPeriods(self.data.constraints, 'c0001')['availablePeriodsNum']
        self.assertEqual(counter, 24)
        counter = self.t.availableNumberOfPeriods(self.data.constraints, 'c0002')['availablePeriodsNum']
        self.assertEqual(counter, 30)

    def test_availableNumberOfPeriods2(self):
        self.t.timeTable[0].append(CellOfTimeTable('c0001', 'B'))
        self.t.timeTable[1].append(CellOfTimeTable('c0002', 'B'))
        self.t.timeTable[2].append(CellOfTimeTable('c0001', 'B'))
        self.t.timeTable[24].append(CellOfTimeTable('c0001', 'B'))
        counter = self.t.availableNumberOfPeriods(self.data.constraints, 'c0001')['availablePeriodsNum']
        self.assertEqual(counter, 21)
        counter = self.t.availableNumberOfPeriods(self.data.constraints, 'c0002')['availablePeriodsNum']
        self.assertEqual(counter, 26)

    def test_availableNumberOfPeriods3(self):
        self.t.timeTable[0].append(CellOfTimeTable('c0001', 'B'))
        self.t.timeTable[1].append(CellOfTimeTable('c0002', 'B'))
        self.t.timeTable[1].append(CellOfTimeTable('c0014', 'C'))
        self.t.timeTable[3].append(CellOfTimeTable('c0014', 'C'))
        self.t.timeTable[2].append(CellOfTimeTable('c0004', 'C'))
        self.t.timeTable[24].append(CellOfTimeTable('c0001', 'B'))
        counter = self.t.availableNumberOfPeriods(self.data.constraints, 'c0001')['availablePeriodsNum']
        self.assertEqual(counter, 21)
        counter = self.t.availableNumberOfPeriods(self.data.constraints, 'c0002')['availablePeriodsNum']
        self.assertEqual(counter, 26)
        counter = self.t.availableNumberOfPeriods(self.data.constraints, 'c0014')['availablePeriodsNum']
        self.assertEqual(counter, 28)
        counter = self.t.availableNumberOfPeriods(self.data.constraints, 'c0071')['availablePeriodsNum']
        self.assertEqual(counter, 15)

    def test_createListOfRooms(self):
        listOfRooms = self.t.createListOfRooms(self.data.rooms, self.data.courses[0].studentsNum)
        self.assertEqual(listOfRooms, set(['B']))
        listOfRooms = self.t.createListOfRooms(self.data.rooms, self.data.courses[1].studentsNum)
        self.assertEqual(listOfRooms, set(['B', 'C']))
        listOfRooms = self.t.createListOfRooms(self.data.rooms, self.data.courses[29].studentsNum)
        self.assertEqual(listOfRooms, set(['B', 'C', 'E', 'F', 'G', 'S']))

    def test_getRoomsIdForCourses(self):
        self.assertEqual(self.t.roomsIdListForCourses['c0014'], set(['B', 'C']))
        self.assertEqual(self.t.roomsIdListForCourses['c0065'], set(['B', 'C', 'E', 'F', 'G', 'S']))

    def test_createNeighbourhoodList(self):
        neighbourhoodList = self.t.createNeighbourhoodList(self.data.curricula, self.data.courses)
        path = u"data/TabuSearchDataTests/neighbourhoodCourses"
        f = open(path, "r")
        self.assertEqual(str(neighbourhoodList), f.readline().strip())

    """Test for list of availablePeriods and availablePairs"""
    def test_availabeNumberOfPeriods4(self):
        periodsList = self.t.availableNumberOfPeriods(self.data.constraints, 'c0001')['availablePeriods']
        self.assertEqual(periodsList, set(range(0, 24)))
        self.t.timeTable[10].append(CellOfTimeTable('c0001', 'B'))
        self.t.timeTable[14].append(CellOfTimeTable('c0014', 'C'))
        self.t.timeTable[14].append(CellOfTimeTable('c0030', 'B'))
        self.t.timeTable[11].append(CellOfTimeTable('c0002', 'B'))
        self.t.timeTable[12].append(CellOfTimeTable('c0004', 'B'))
        result = self.t.availableNumberOfPeriods(self.data.constraints, 'c0001')

        self.assertEqual(result['availablePeriods'], set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]))
        self.assertEqual(result['availablePairsNum'], 20)
        result = self.t.availableNumberOfPeriods(self.data.constraints, 'c0002')
        self.assertEqual(result['availablePairsNum'], 52)

        self.t.timeTable[13].append(CellOfTimeTable('c0057', 'E'))
        result = self.t.availableNumberOfPeriods(self.data.constraints, 'c0002')
        self.assertEqual(result['availablePairsNum'], 52)

        self.t.timeTable[13].append(CellOfTimeTable('c0066', 'B'))
        self.t.timeTable[15].append(CellOfTimeTable('c0005', 'B'))
        result = self.t.availableNumberOfPeriods(self.data.constraints, 'c0002')
        self.assertEqual(result['availablePairsNum'], 49)
        self.assertEqual(result['availablePeriodsNum'], 26)
if __name__=="__main__":
    unittest.main()
