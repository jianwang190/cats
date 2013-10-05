import unittest
from cats.readers.competition import CompetitionReader

class ReadTest(unittest.TestCase):
    def test_read(self):
        c = CompetitionReader(1)
        self.assertEquals(c.getInstanceName(), "Fis0506-1")
        self.assertEquals(c.getConstraintNum(), len(c.constraints))
        self.assertEquals(c.getCoursesNum(), len(c.courses))
        self.assertEquals(c.getCurriculumNum(), len(c.curricula))
        self.assertEquals(c.getRoomsNum(), len(c.rooms))

if __name__=="__main__":
    unittest.main()
