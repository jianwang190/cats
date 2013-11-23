__author__ = 'filip'
from cats.ga.geneticAlgorithm import GeneticAlgorithm
from cats.utils.timetable import TimeTableFactory
from cats.readers.competitionReader import CompetitionDictReader
import random
import sys

class GATest(object):
    def setUp(self):
        self.c = CompetitionDictReader()
        self.data = self.c.readInstance(1)
        self.solutions = dict()
        self.fitnessTable = dict()
        self.populationSize = 10
        for it in range(self.populationSize):
            self.solutions[it] = TimeTableFactory.getTimeTable(self.data)

        self.ga = GeneticAlgorithm(self.data, self.solutions, self.populationSize, 0.01, 7)
        self.ga.generateInitialSolutions()
        self.ga.estimateFitness()

        for epoch in range(10):
            self.ga.nextGeneration("tournament")
            self.ga.mutate()
            self.ga.estimateFitness()
            print "Epoka:", epoch, "najlepszy wynik:", self.ga.fitnessTable[self.ga.getTopSolutionIndex()]

        self.ga.saveBestTimeTableToFile("/home/filip/Inzynierka/cats/plan" + str(random.randint(0, 10000)) + ".txt")
        """
        for solutionId in self.solutions.keys():
            print "SolutionId: ", solutionId
            for slot in self.solutions[solutionId].timeTable.keys():
                sys.stdout.write("Slot id: " + str(slot))
                for pair in self.solutions[solutionId].timeTable[slot]:
                    sys.stdout.write(pair[0] + " " + pair[1] + "; ")
                print " "
        """

if __name__=="__main__":
    t=GATest()
    t.setUp()



