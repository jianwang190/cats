from cats.ga.geneticAlgorithm import GeneticAlgorithm

__author__ = 'tomek'
import time
import sys


from cats.readers.competitionReader import  CompetitionDictReader


fileName = sys.argv[1]
timeLimit = float(sys.argv[2])


c = CompetitionDictReader()
data = c.read(fileName)

ga = GeneticAlgorithm(data, timeLimit)
