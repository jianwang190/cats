import unittest
from cats.adaptiveTabuSearch import softConstraints
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
        assignedList = [(0, 'c0001', 'E'), (1, 'c0001', 'B'), (4, 'c0001', 'C'), (7, 'c0002', 'G'), (9, 'c0072', 'E')]
        self.t.addDataToTimetable(assignedList)
        penalty = softConstraints.softConstraintsPenalty(self.t.getTimeTable(), self.data, 'c0001')['penaltyCurriculumCompactness']
        self.assertEqual(penalty, 6)

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
        assignedList = [(0, 'c0001', 'E'), (1, 'c0001', 'B'), (4, 'c0001', 'C'), (7, 'c0002', 'G'), (9, 'c0072', 'E')]
        self.t.addDataToTimetable(assignedList)
        result = softConstraints.softConstraintsPenalty(self.t.getTimeTable(), self.data, 'c0001')
        penalty = result['penaltyRoomStability']
        self.assertEqual(penalty, 2)
        penalty = result['penaltyRoomCapacity']
        self.assertEqual(penalty, 151)
        penalty = result['penaltyMinWorkingDays']
        self.assertEqual(penalty, 0)
        penalty = result['penaltyCurriculumCompactness']
        self.assertEqual(penalty, 6)
        penalty = softConstraints.totalSoftConstraintsPenalty(self.t.getTimeTable(), self.data, 'c0001')
        self.assertEqual(penalty, 159)
        result = softConstraints.softConstraintsPenalty(self.t.getTimeTable(), self.data, 'c0072')['penaltyCurriculumCompactness']
        self.assertEqual(result, 4)



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
        penalty = softConstraints.softConstraintsPenalty(self.t.getTimeTable(), self.data, 'c0001')['penaltyCurriculumCompactness']
        self.assertEqual(penalty, 10)
        penalty = softConstraints.softConstraintsPenalty(self.t.getTimeTable(), self.data, 'c0004')['penaltyCurriculumCompactness']
        self.assertEqual(penalty, 14)
        penalty = softConstraints.totalSoftConstraintsPenalty(self.t.getTimeTable(), self.data, 'c0001')
        self.assertEqual(penalty, 363)
        penalty = softConstraints.totalSoftConstraintsPenalty(self.t.getTimeTable(), self.data, 'c0004')
        self.assertEqual(penalty, 102)
        penalty = softConstraints.totalSoftConstraintsPenalty(self.t.getTimeTable(), self.data, 'c0072')
        self.assertEqual(penalty, 16)

    def testTotalSoftConstraintsForTimetable(self):
        assignedList = [(0, 'c0001', 'E')]
        self.t.addDataToTimetable(assignedList)
        penalty = softConstraints.totalSoftConstraintsForTimetable(self.t.getTimeTable(), self.data)
        self.assertEqual(penalty, 137)

