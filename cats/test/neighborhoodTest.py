import unittest
from cats.utils.timetable import TimeTable, CellOfTimeTable, TimeTableFactory
from cats.readers.competitionReader import CompetitionReader
from cats.tabuSearch.tabuSearch import TabuSearch
class NeighborhoodTest(unittest.TestCase):
    def setUp(self):
        self.c = CompetitionReader()
        self.data = self.c.readInstance(1)
        self.t = TimeTableFactory.getTimeTable(self.data)
        self.tabuSearch = TabuSearch()

    def test_createLeftRightLists(self):
        self.t.timeTable[0].append(CellOfTimeTable('c0001', 'B'))
        self.t.timeTable[0].append(CellOfTimeTable('c0014', 'C'))
        self.t.timeTable[0].append(CellOfTimeTable('c0072', 'E'))
        result = self.tabuSearch.createLeftRightLists(self.t.roomsIdListForCourses, self.t.timeTable[0])
        leftNodes = {'c0014' : set(['C', 'B']), 'c0072' : set(['C', 'B', 'E', 'G', 'F', 'S']), 'c0001' : set(['B'])}
        rightNodes = {'C': ['c0014', 'c0072'], 'B': ['c0014', 'c0072', 'c0001'], 'E' : ['c0072'], 'G': ['c0072'], 'F': ['c0072'], 'S': ['c0072']}
        self.assertEqual(result['leftNodes'], leftNodes)
        self.assertEqual(result['rightNodes'], rightNodes)
        self.assertEqual(result['totalEdgeNumber'], 9)

    def test_deleteEdges(self):
        self.t.timeTable[0].append(CellOfTimeTable('c0001', 'B'))
        self.t.timeTable[0].append(CellOfTimeTable('c0014', 'C'))
        self.t.timeTable[0].append(CellOfTimeTable('c0072', 'E'))
        result = self.tabuSearch.createLeftRightLists(self.t.roomsIdListForCourses, self.t.timeTable[0])
        leftNodes = result['leftNodes']
        rightNodes = result['rightNodes']
        graph = self.tabuSearch.deleteEdges(leftNodes, rightNodes, 'c0014', 'C')
        self.assertEqual(graph['leftNodes'],{'c0072': set(['B', 'E', 'G', 'F', 'S']), 'c0001': set(['B'])})
        self.assertEqual(graph['rightNodes'], {'B' : ['c0072', 'c0001'], 'E': ['c0072'], 'G': ['c0072'], 'F' : ['c0072'], 'S': ['c0072']})
        self.assertEqual(graph['totalEdgeNumber'], 6)

    def test_findMin(self):
        self.t.timeTable[0].append(CellOfTimeTable('c0001', 'B'))
        self.t.timeTable[0].append(CellOfTimeTable('c0014', 'C'))
        self.t.timeTable[0].append(CellOfTimeTable('c0072', 'E'))
        result = self.tabuSearch.createLeftRightLists(self.t.roomsIdListForCourses, self.t.timeTable[0])
        leftNodes = result['leftNodes']
        rightNodes = result['rightNodes']
        roomId = self.tabuSearch.findMin(rightNodes, leftNodes, 'c0014')
        self.assertEqual(roomId, 'C')
        roomId = self.tabuSearch.findMin(rightNodes, leftNodes, 'c0001')
        self.assertEqual(roomId, 'B')
        roomId = self.tabuSearch.findMin(rightNodes, leftNodes, 'c0072')
        self.assertEqual(roomId, 'E')

    def test_maximumMatching(self):
        self.t.timeTable[0].append(CellOfTimeTable('c0001', 'B'))
        self.t.timeTable[0].append(CellOfTimeTable('c0014', 'C'))
        self.t.timeTable[0].append(CellOfTimeTable('c0072', 'E'))
        result = self.tabuSearch.maximumMatching(self.t.roomsIdListForCourses, self.t.timeTable[0])
        self.assertEqual(result, [['c0001', 'B'], ['c0014', 'C'], ['c0072', 'E']])
if __name__=="__main__":
    unittest.main()
