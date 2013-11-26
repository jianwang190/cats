__author__ = 'filip'
from cats.ga.geneticAlgorithm import GeneticAlgorithm
from cats.utils.timetable import TimeTableFactory
from cats.readers.competitionReader import CompetitionDictReader
from cats.ga.checkHardConstraints import countHardConstraints
import random
import sys

class GATest(object):
    def setUp(self):
        self.c = CompetitionDictReader()
        self.data = self.c.readInstance(1)
        self.solutions = dict()
        self.fitnessTable = dict()
        self.populationSize = 20
        for it in range(self.populationSize):
            self.solutions[it] = TimeTableFactory.getTimeTable(self.data)

        self.ga = GeneticAlgorithm(self.data, self.solutions, self.populationSize, 20, 0.01, 5)
        self.ga.generateInitialSolutions()
        self.ga.estimateFitness()

        #self.ga.runAlgorithmLoop()

        #self.ga.saveBestTimeTableToFile("/home/filip/Inzynierka/cats/Plany/plan" + str(random.randint(0, 10000)) + ".sln")

if __name__=="__main__":
    t=GATest()
    t.setUp()



