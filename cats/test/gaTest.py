__author__ = 'filip'
from cats.ga.geneticAlgorithm import GeneticAlgorithm
from cats.readers.competitionReader import CompetitionDictReader

class GATest(object):
    def Run(self):
        self.c = CompetitionDictReader()
        self.data = self.c.readInstance(22)
        self.ga = GeneticAlgorithm(self.data)

if __name__=="__main__":
    t = GATest()
    t.Run()

