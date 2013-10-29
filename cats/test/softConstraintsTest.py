import unittest
from cats.tabuSearch import softConstraints
from cats.readers.competitionReader import CompetitionReader, CompetitionDictReader
from cats.utils.timetable import TimeTableFactory, CellOfTimeTable


class softConstraintsTest(unittest.TestCase):
    def setUp(self):
        self.c = CompetitionDictReader()
        self.data = self.c.readInstance(1)
        self.t = TimeTableFactory.getTimeTable(self.data)


    """Test soft penalty for room capacity"""
    def testSoftConstraintsRoomCapacity(self):
        assignedList = [(0, 'c0001', 'E'), (1, 'c0002', 'B'), (2, 'c0001', 'B'), (24, 'c0001', 'B')]
        self.t.addDataToTimetable(assignedList)
        penalty = softConstraints.penaltyRoomCapacity(self.data, 'c0001', ['E'])
        self.assertEqual(penalty, 121)
        penalty = softConstraints.penaltyRoomCapacity(self.data, 'c0002', ['B'])
        self.assertEqual(penalty, 0)
        penalty = softConstraints.penaltyRoomCapacity(self.data, 'c0001', ['B'])
        self.assertEqual(penalty, 0)
        penalty = softConstraints.penaltyRoomCapacity(self.data, 'c0072', ['B'])
        self.assertEqual(penalty, 0)
        penalty = softConstraints.penaltyRoomCapacity(self.data, 'c0001', ['E', 'E', 'G'])
        self.assertEqual(penalty, 352)

    """Test for soft constraints function counting minimum working days"""
    def testSoftConstraintsMinimumWorkingDays(self):
        assignedList = [(0, 'c0001', 'E'), (1, 'c0001', 'B'), (2, 'c0001', 'B'), (3, 'c0001', 'B'), (0, 'c0004', 'B'), (1, 'c0004', 'B'), (2, 'c0004', 'B')]
        self.t.addDataToTimetable(assignedList)
        penalty = softConstraints.softConstraintsPenalty(self.t.getTimeTable(), self.data, 'c0001')['penaltyMinWorkingDays']
        self.assertEqual(penalty, 5)
        penalty = softConstraints.softConstraintsPenalty(self.t.getTimeTable(), self.data, 'c0004')['penaltyMinWorkingDays']
        self.assertEqual(penalty, 0)
        assignedList = [(3, 'c0004', 'B'), (4, 'c0004', 'B'), (5, 'c0004', 'B')]
        self.t.addDataToTimetable(assignedList)
        penalty = softConstraints.softConstraintsPenalty(self.t.getTimeTable(), self.data, 'c0004')['penaltyMinWorkingDays']
        self.assertEqual(penalty, 5)
        assignedList = [(12, 'c0004', 'B'), (4, 'c0001', 'B'), (5, 'c0001', 'B')]
        self.t.addDataToTimetable(assignedList)
        penalty = softConstraints.softConstraintsPenalty(self.t.getTimeTable(), self.data, 'c0004')['penaltyMinWorkingDays']
        self.assertEqual(penalty, 5)
        penalty = softConstraints.softConstraintsPenalty(self.t.getTimeTable(), self.data, 'c0001')['penaltyMinWorkingDays']
        self.assertEqual(penalty, 15)
        penalty = softConstraints.softConstraintsPenalty(self.t.getTimeTable(), self.data, 'c0072')['penaltyMinWorkingDays']
        self.assertEqual(penalty, 0)

    """Test for soft constraints function counting penalty for room stability"""
    def testSoftConstraintsRoomStability(self):
        assignedList = [(0, 'c0001', 'E'), (1, 'c0001', 'B'), (2, 'c0001', 'C'), (3, 'c0001', 'G'), (0, 'c0004', 'B'), (1, 'c0004', 'B'), (2, 'c0004', 'B')]
        self.t.addDataToTimetable(assignedList)
        penalty = softConstraints.softConstraintsPenalty(self.t.getTimeTable(), self.data, 'c0001')['penaltyRoomStability']
        self.assertEqual(penalty, 3)
        penalty = softConstraints.softConstraintsPenalty(self.t.getTimeTable(), self.data, 'c0004')['penaltyRoomStability']
        self.assertEqual(penalty, 0)
        penalty = softConstraints.softConstraintsPenalty(self.t.getTimeTable(), self.data, 'c0072')['penaltyRoomStability']
        self.assertEqual(penalty, 0)

    """Test for soft constraints penalty for curriculum compactness"""
    def testSoftConstraintsCurriculumCompactness(self):
        assignedList = [(0, 'c0001', 'E', ['q0001']), (1, 'c0001', 'B', ['q0001']), (4, 'c0001', 'C', ['q0001']), (7, 'c0002', 'G', ['q0001']), (9, 'c0072', 'E', ['q0002'])]
        self.t.addDataToTimetable(assignedList)
        penalty = softConstraints.softConstraintsPenalty(self.t.getTimeTable(), self.data, 'c0001', 'q0001')['penaltyCurriculumCompactness']
        self.assertEqual(penalty, 4)

    """Test for helper function to count curriculum compactness"""
    def testCountPenaltyForCurriculumCompactness(self):
        penalty = softConstraints.countPenaltyForCurriculumCompactness([0, 1, 4, 7], 6)
        self.assertEqual(penalty, 4)
        penalty = softConstraints.countPenaltyForCurriculumCompactness([0, 1, 4, 7, 8, 20, 29], 6)
        self.assertEqual(penalty, 6)
        penalty = softConstraints.countPenaltyForCurriculumCompactness([0, 1, 2, 4, 5, 6, 7], 4)
        self.assertEqual(penalty, 0)
        penalty = softConstraints.countPenaltyForCurriculumCompactness([0, 1, 3, 4, 5, 6, 7], 4)
        self.assertEqual(penalty, 2)

    def testTotalSoftConstrainsPenalty(self):
        assignedList = [(0, 'c0001', 'E', ['q0001']), (1, 'c0001', 'B', ['q0001']), (4, 'c0001', 'C', ['q0001']), (7, 'c0002', 'G', ['q0001']), (9, 'c0072', 'E', ['q0002'])]
        self.t.addDataToTimetable(assignedList)
        result = softConstraints.softConstraintsPenalty(self.t.getTimeTable(), self.data, 'c0001', 'q0001')
        penalty = result['penaltyRoomStability']
        self.assertEqual(penalty, 2)
        penalty = result['penaltyRoomCapacity']
        self.assertEqual(penalty, 151)
        penalty = result['penaltyMinWorkingDays']
        self.assertEqual(penalty, 0)
        penalty = result['penaltyCurriculumCompactness']
        self.assertEqual(penalty, 4)
        penalty = softConstraints.totalSoftConstraintsPenalty(self.t.getTimeTable(), self.data, 'c0001', 'q0001')
        self.assertEqual(penalty, 157)

    def testTotalSoftConstraintsPenalty2(self):
        path = u"data/TabuSearchDataTests/softConstraintsLectures"
        self.t.readLecturesToTimetable(path)
        coursesId = ['c0001', 'c0004', 'c0072', 'c0071']
        penalty = sum(map(lambda x: softConstraints.softConstraintsPenalty(self.t.getTimeTable(), self.data, x)['penaltyRoomStability'], coursesId))
        self.assertEqual(penalty, 4)
        penalty = sum(map(lambda x: softConstraints.softConstraintsPenalty(self.t.getTimeTable(), self.data, x)['penaltyRoomCapacity'], coursesId))
        self.assertEqual(penalty, 440)
        penalty = sum(map(lambda x: softConstraints.softConstraintsPenalty(self.t.getTimeTable(), self.data, x)['penaltyMinWorkingDays'], coursesId))
        self.assertEqual(penalty, 10)
        penalty = softConstraints.softConstraintsPenalty(self.t.getTimeTable(), self.data, 'c0001', 'q0001')['penaltyCurriculumCompactness']
        self.assertEqual(penalty, 8)
        penalty = softConstraints.totalSoftConstraintsPenalty(self.t.getTimeTable(), self.data, 'c0001', 'q0001')
        self.assertEqual(penalty, 361)
        penalty = softConstraints.totalSoftConstraintsPenalty(self.t.getTimeTable(), self.data, 'c0004', 'q0001')
        self.assertEqual(penalty, 96)
        penalty = softConstraints.totalSoftConstraintsPenalty(self.t.getTimeTable(), self.data, 'c0072', 'q0008')
        self.assertEqual(penalty, 14)
