import unittest
from cats.ga.geneticAlgorithm import GeneticAlgorithm
from cats.utils.timetable import TimeTableFactory
from cats.readers.competitionReader import CompetitionReader


class GeneticTest(object):
    def setUp(self):
        self.c = CompetitionReader()
        self.data = self.c.readInstance(1)
        self.solutions = dict()
        self.fitnessTable = dict()
        self.populationSize = 50
        for it in range(self.populationSize):
            self.solutions[it] = TimeTableFactory.getTimeTable(self.data)
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
        self.ga = GeneticAlgorithm(self.data, self.solutions, self.populationSize, 0.1)
        self.solutions = self.ga.generateInitialSolutions()
        self.fitnessTable = self.ga.estimateFitness(self.solutions)

        for epoch in range(20):
            self.solutions = self.ga.nextGeneration(self.solutions, "random")
            self.solutions = self.ga.mutate(self.solutions)
            self.fitnessTable = self.ga.estimateFitness(self.solutions)

        for slot in self.t.timeTable.keys():
            print "Slot id:", slot
            for pair in self.t.timeTable[slot]:
                print pair.courseId, pair.roomId



if __name__=="__main__":
    #unittest.main()
    t= GeneticTest()
    t.setUp()