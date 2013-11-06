__author__ = 'tomek'
from unittest import TestCase
from cats.readers.competitionReader import CompetitionDictReader
from cats.utils.timetable import TimeTable, TimeTableFactory
from cats.adaptiveTabuSearch.advancedNeighborhood import AdvancedNeighborhood

class AdvancedNeighborhoodTest(TestCase):
    def setUp(self):
        self.c = CompetitionDictReader()
        self.data = self.c.readInstance(1)
        self.t = TimeTableFactory.getTimeTable(self.data)
        assigned = [(0, 'c0030', 'B'),\
                    (0, 'c0033', 'B'),\
                    (1, 'c0031', 'B'),\
                    (1, 'c0032', 'B'),\
                    (0, 'c0065', 'B'),\
                    (0, 'c0062', 'B'),\
                    (0, 'c0058', 'B'),\
                    (0, 'c0057', 'B'),\
                    (1, 'c0059', 'B'),\
                    (1, 'c0067', 'B'),\
                    (1, 'c0061', 'B'),\
                    (1, 'c0071', 'B'),\

            ]
        self.t.addDataToTimetable(assigned)


    def testGenerateChain(self):


        a = AdvancedNeighborhood()
        chains = a.generateChains(self.t, 0, 1)
        expected = {
            1: ["c0030", "c0031", "c0032", "c0033"],
            2: ["c0057", "c0059", "c0065"],
            3: ["c0061", "c0062", "c0071"],
            4: ["c0058"],
            5: ["c0067"]
        }
        for a in chains:
            self.assertSequenceEqual(sorted(chains[a]), sorted(expected[a]))

    def testGeneratePairs(self):
        a = AdvancedNeighborhood()
        chains = a.generateChains(self.t, 0, 1)
        pairs = a.generatePossibleSwappingPairs(self.t, chains)
        print pairs

    def testKempeSwap(self):
        a = AdvancedNeighborhood()
        chains = a.generateChains(self.t, 0, 1)
        n = a.kempeSwap(self.t, 0, 1 ,(set(chains[2]), set(chains[3])))
        for i in n[0]:
            print i.courseId, i.roomId
        print
        for i in n[1]:
            print i.courseId, i.roomId