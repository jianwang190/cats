
import unittest
from cats.utils.timetable import TimeTable, TimeTableFactory
from cats.readers.competitionReader import CompetitionDictReader
from cats.adaptiveTabuSearch.perturbation import selectRandom, rankingOfLectures



class PerturbationTest(unittest.TestCase):
    def setUp(self):
        self.c = CompetitionDictReader()
        self.data = self.c.readInstance(1)
        self.t = TimeTableFactory.getTimeTable(self.data)
        "Create sorted list of rooms (sorted by capacity)"
        self.sortedRoomIdList = sorted(self.data.getAllRooms(), key=lambda room: room.capacity, reverse=True)

    def testSelectRandom(self):
        listItems = [('c5', 0), ('c1', 1), ('c6', 3), ('c4', 2), ('c4', 9), ('c2', 8)]
        selectedValues = selectRandom(listItems, 5)
        selectedValuesSet = set(selectedValues)
        self.assertEqual(len(selectedValues), 5)
        self.assertEqual(len(selectedValuesSet), 5)

    def testRankingOfLectures(self):
        path = u"data/TabuSearchDataTests/softConstraintsLectures"
        self.t.readLecturesToTimetable(path)
        n = 4
        q = 13
        selectedValues = rankingOfLectures(self.t.getTimeTable(), self.data, n, q)
        uniqueSelectedValues = set(selectedValues)
        self.assertEqual(len(uniqueSelectedValues), len(selectedValues))



if __name__=="__main__":
    unittest.main()