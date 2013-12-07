#!/usr/bin/env python

from cats.adaptiveTabuSearch.tabuSearch import AdaptiveTabuSearch
from cats.readers.competitionReader import CompetitionDictReader
__author__ = 'tomek'

def main():
    c= CompetitionDictReader()
    data = c.readInstance(1)
    a = AdaptiveTabuSearch(data, 600)
    t = a.run()
    i = 1
    o = file('result'+str(i), 'w')

    o.close()

if __name__=="__main__":
    main()
