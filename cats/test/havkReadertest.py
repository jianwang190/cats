import unittest
from cats.readers.competitionReader import CompetitionReader
from cats.utils.data import Data

class ReadTest(unittest.TestCase):
    def setUp(self):
        self.c = CompetitionReader()
        self.data = self.c.readInstance(1)

    def test_header(self):
        self.assertEquals(self.data.instanceName, "Fis0506-1")
        self.assertEquals(self.data.daysNum, 5)
        self.assertEquals(self.data.periods_per_day, 6)

    def test_courses(self):
        self.assertEquals(self.data.courses[0].id, 'c0001')
        self.assertEquals(self.data.courses[0].teacher, 't000')
        self.assertEquals(self.data.courses[0].lectureNum, 6)
        self.assertEquals(self.data.courses[0].minWorkingDays, 4)
        self.assertEquals(self.data.courses[0].studentsNum, 130)
    def test_rooms(self):
        self.assertEquals(self.data.rooms[0].id, 'B')
        self.assertEquals(self.data.rooms[0].capacity, 200)

    def test_curriculum(self):
        self.assertEquals(self.data.curricula[0].id, 'q000')
        self.assertEquals(self.data.curricula[0].courseNum, 4)
        self.assertListEqual(self.data.curricula[0].members, ['c0001', 'c0002', 'c0004', 'c0005'])


if __name__=="__main__":
    unittest.main()
