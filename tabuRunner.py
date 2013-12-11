#!/usr/bin/env python

from cats.adaptiveTabuSearch.tabuSearch import AdaptiveTabuSearch
from cats.readers.competitionReader import CompetitionDictReader

def main():
    c= CompetitionDictReader()
    numberOfInstance = 3
    data = c.readInstance(numberOfInstance)
    a = AdaptiveTabuSearch(data, 960)

    bestSolution = a.run()
    o = file('result'+str(numberOfInstance ) + str('add'), 'w')
    for slot in bestSolution.getTimeTable():
        for lecture in bestSolution.getTimeTable()[slot]:
            tuple = (slot/data.periodsPerDay, slot % data.periodsPerDay)
            line = lecture[0] + ' ' + lecture[1] + ' ' + str(tuple[0])+ ' ' + \
                str(tuple[1]) + '\n'
            o.write(line)
    o.close()

if __name__=="__main__":
    main()
