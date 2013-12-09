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

        self.ga = GeneticAlgorithm(self.data, self.solutions, self.populationSize, 0.01)
        self.solutions = self.ga.generateInitialSolutions()
        self.fitnessTable = self.ga.estimateFitness(self.solutions)

        for epoch in range(20):
            self.solutions = self.ga.nextGeneration(self.solutions, "random")
            self.solutions = self.ga.mutate(self.solutions)
            self.fitnessTable = self.ga.estimateFitness(self.solutions)
            print self.fitnessTable[self.ga.getTopSolutionIndex()]

        for solutionId in self.solutions.keys():
            print "SolutionId: ", solutionId
            for slot in self.solutions[solutionId].timeTable.keys():
                print "Slot id:", slot
                for pair in self.solutions[solutionId].   timeTable[slot]:
                    print pair[0], pair[1]



if __name__=="__main__":
    #unittest.main()
    t=GeneticTest()
    t.setUp()