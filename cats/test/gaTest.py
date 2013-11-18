__author__ = 'filip'
from cats.ga.geneticAlgorithm import GeneticAlgorithm
from cats.utils.timetable import TimeTableFactory
from cats.readers.competitionReader import CompetitionDictReader

class GATest(object):
    def setUp(self):
        self.c = CompetitionDictReader()
        self.data = self.c.readInstance(1)
        self.solutions = dict()
        self.fitnessTable = dict()
        self.populationSize = 3
        for it in range(self.populationSize):
            self.solutions[it] = TimeTableFactory.getTimeTable(self.data)

        self.ga = GeneticAlgorithm(self.data, self.solutions, self.populationSize, 0.01)
        self.solutions = self.ga.generateFirstSolutions(self.solutions)
        self.fitnessTable = self.ga.estimateFitness(self.solutions)

        for epoch in range(int(self.ga.iterationsMax)):
            self.solutions = self.ga.nextGeneration(self.solutions, self.fitnessTable, "random")
            self.solutions = self.ga.mutate(self.solutions, self.fitnessTable)
            self.fitnessTable = self.ga.estimateFitness(self.solutions)
            print self.fitnessTable[self.ga.getTopSolution(self.fitnessTable)]

        for solutionId in self.solutions.keys():
            print "SolutionId: ", solutionId
            for slot in self.solutions[solutionId].timeTable.keys():
                print "Slot id:", slot
                for pair in self.solutions[solutionId].timeTable[slot]:
                    print pair[0], pair[1]


if __name__=="__main__":
    t=GATest()
    t.setUp()



