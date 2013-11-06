import unittest
from cats.ga.geneticAlgorithm import GeneticAlgorithm
from cats.utils.timetable import TimeTableFactory
from cats.readers.competitionReader import CompetitionReader


class GeneticTest(object):
    def setUp(self):
        self.c = CompetitionReader()
        self.data = self.c.readInstance(1)
        self.t = TimeTableFactory.getTimeTable(self.data)
        #print self.t.getValueSlot(1,1)
        #print "sdfsdf"
        #for slot in self.t.timeSlots:
        #    print slot
        #for kurs in self.t.neighbourhoodList.keys():
        #    print "klucz", kurs
        #    for konflikty in self.t.neighbourhoodList[kurs]:
        #        print konflikty
        #print "sdfsdfsdf"
        #for kursy in self.t.roomsIdListForCourses:
        #    print "SDSDS", kursy
        #    for room in self.t.roomsIdListForCourses[kursy]:
        #        print room
        self.ga = GeneticAlgorithm(self.data)
        self.ga.generateInitialSolution()
        for slot in self.ga.timeTable.timeTable:
            print "Slot id:", slot
            for info in slot:
                print info



if __name__=="__main__":
    #unittest.main()
    t= GeneticTest()
    t.setUp()