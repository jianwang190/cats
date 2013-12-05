import unittest
from cats.adaptiveTabuSearch.heuristics import initialSolution
import os
from cats.utils.timetable import TimeTable, TimeTableFactory
from cats.readers.competitionReader import CompetitionReader, CompetitionDictReader
from random import randint
from cats.utils.data import Data

class DataSchoolTest(unittest.TestCase):
    def setUp(self):
        self.c = CompetitionDictReader()
        self.data = self.c.readInstance(22)

        self.t = TimeTableFactory.getTimeTable(self.data)

    #def test_initial(self):
    #    #for x in self.data.courses.keys():
    #    #    course = self.data.courses[x]
    #    #    print course.id, course.lectureNum, course.minWorkingDays, course.studentsNum
    #    pass

    #def test_tabu(self):
    #    #self.t.jsonify()
    #    print "Dane ze szkoly test"
    #    initialSolution(self.t, self.data)


if __name__=="__main__":
    unittest.main()