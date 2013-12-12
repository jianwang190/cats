from cats.adaptiveTabuSearch.tabuSearch import AdaptiveTabuSearch

__author__ = 'tomek'
import time
import sys


from cats.readers.competitionReader import  CompetitionDictReader


fileName = sys.argv[1]
timeLimit = float(sys.argv[2])


c = CompetitionDictReader()
data = c.read(fileName)

a = AdaptiveTabuSearch(data, 2400)
bestSolution = a.run()

for slot in bestSolution.getTimeTable():
    for lecture in bestSolution.getTimeTable()[slot]:
        tuple = (slot/data.periodsPerDay, slot % data.periodsPerDay)
        print lecture[0] + ' ' + lecture[1] + ' ' + str(tuple[0])+ ' ' + \
            str(tuple[1])


