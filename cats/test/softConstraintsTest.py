import unittest
from cats.readers.competitionReader import CompetitionReader, CompetitionDictReader
from cats.utils.timetable import TimeTableFactory
from cats.adaptiveTabuSearch import softConstraints2


class softConstraintsTest(unittest.TestCase):
    def setUp(self):
        self.c = CompetitionDictReader()
        self.data = self.c.readInstance(1)
        self.t = TimeTableFactory.getTimeTable(self.data)

    """Test for soft constraints function counting minimum working days"""
    def testSoftConstraintsMinimumWorkingDays(self):
        assignedList = [(0, 'c0001', 'E'), (1, 'c0001', 'B'), (2, 'c0001', 'B'), (3, 'c0001', 'B'), (0, 'c0004', 'B'), (1, 'c0004', 'B'), (2, 'c0004', 'B')]
        self.t.addDataToTimetable(assignedList)
        penalty = softConstraints2.softConstraintsPenalty(self.t.getTimeTable(), self.data)['penaltyMinWorkingDays']
        self.assertEqual(penalty, 520)
        assignedList = [(3, 'c0004', 'B'), (4, 'c0004', 'B'), (5, 'c0004', 'B')]
        self.t.addDataToTimetable(assignedList)
        penalty = softConstraints2.softConstraintsPenalty(self.t.getTimeTable(), self.data)['penaltyMinWorkingDays']
        self.assertEqual(penalty, 520)
        assignedList = [(12, 'c0004', 'B'), (4, 'c0001', 'B'), (5, 'c0001', 'B')]
        self.t.addDataToTimetable(assignedList)
        penalty = softConstraints2.softConstraintsPenalty(self.t.getTimeTable(), self.data)['penaltyMinWorkingDays']
        self.assertEqual(penalty, 515)

    """Test for soft constraints function counting penalty for room stability"""
    def testSoftConstraintsRoomStability(self):
        assignedList = [(0, 'c0001', 'E'), (1, 'c0001', 'B'), (2, 'c0001', 'C'), (3, 'c0001', 'G'), (0, 'c0004', 'B'), (1, 'c0004', 'B'), (2, 'c0004', 'B')]
        self.t.addDataToTimetable(assignedList)
        penalty = softConstraints2.softConstraintsPenalty(self.t.getTimeTable(), self.data)['penaltyRoomStability']
        self.assertEqual(penalty, 3)


    """Test for soft constraints penalty for curriculum compactness"""
    def testSoftConstraintsCurriculumCompactness(self):
        assignedList = [(0, 'c0001', 'E'), (1, 'c0001', 'B'), (4, 'c0001', 'C'), (7, 'c0002', 'G'), (9, 'c0072', 'E')]
        self.t.addDataToTimetable(assignedList)
        penalty = softConstraints2.softConstraintsPenalty(self.t.getTimeTable(), self.data)['penaltyCurriculumCompactness']
        self.assertEqual(penalty, 10)

    """Test for helper function to count curriculum compactness"""
    def testCountPenaltyForCurriculumCompactness(self):
        penalty = softConstraints2.countPenaltyForCurriculumCompactness([0, 1, 4, 7], 6)
        self.assertEqual(penalty, 2)
        penalty = softConstraints2.countPenaltyForCurriculumCompactness([0, 1, 4, 7, 8, 20, 29], 6)
        self.assertEqual(penalty, 3)
        penalty = softConstraints2.countPenaltyForCurriculumCompactness([0, 1, 2, 4, 5, 6, 7], 4)
        self.assertEqual(penalty, 0)
        penalty = softConstraints2.countPenaltyForCurriculumCompactness([0, 1, 3, 4, 5, 6, 7], 4)
        self.assertEqual(penalty, 1)

    def testTotalSoftConstrainsPenalty(self):
        assignedList = [(0, 'c0001', 'E'), (1, 'c0001', 'B'), (4, 'c0001', 'C'), (7, 'c0002', 'G'), (9, 'c0072', 'E')]
        self.t.addDataToTimetable(assignedList)
        penalty = softConstraints2.softConstraintsPenalty(self.t.getTimeTable(), self.data)['penaltyCurriculumCompactness']
        self.assertEqual(penalty, 10)


    def testTotalSoftConstraintsPenalty2(self):
        expectedResult = reduce(lambda x, y: x + y, map(lambda z: z.minWorkingDays, self.data.getAllCourses())) * 5
        penalty = softConstraints2.softConstraintsPenalty(self.t.getTimeTable(), self.data)['penaltyMinWorkingDays']
        self.assertEqual(penalty, expectedResult)

        path = u"data/TabuSearchDataTests/softConstraintsLectures"
        self.t.readLecturesToTimetable(path)
        penalty = softConstraints2.softConstraintsPenalty(self.t.getTimeTable(), self.data)['penaltyRoomStability']
        self.assertEqual(penalty, 4)
        penalty = softConstraints2.softConstraintsPenalty(self.t.getTimeTable(), self.data)['penaltyRoomCapacity']
        self.assertEqual(penalty, 440)
        penalty = softConstraints2.softConstraintsPenalty(self.t.getTimeTable(), self.data)['penaltyMinWorkingDays']
        self.assertEqual(penalty, 490)
        penalty = softConstraints2.softConstraintsPenalty(self.t.getTimeTable(), self.data)['penaltyCurriculumCompactness']
        self.assertEqual(penalty, 24)
        penalty = softConstraints2.softConstraintsPenalty(self.t.getTimeTable(), self.data)['totalPenalty']
        self.assertEqual(penalty, 958)


    """Perturbation penalty"""
    def testSoftConstraintsRoomStability22(self):
        assignedList = [(0, 'c0001', 'E'), (1, 'c0001', 'B'), (2, 'c0001', 'C'), (3, 'c0001', 'G'), (0, 'c0004', 'B'), (1, 'c0004', 'B'), (2, 'c0004', 'B')]
        self.t.addDataToTimetable(assignedList)
        result = softConstraints2.softConstraintsPenalty(self.t.getTimeTable(), self.data, "perturbation")
        penaltyRoomStability = result['penaltyRoomStability']
        self.assertEqual(penaltyRoomStability, 3)
        self.assertEqual(len(result['perturbationPenalty']), len((assignedList)))


    """Perturbation"""
    def testSoftConstraintsPerturbation(self):
        assignedList = [(0, 'c0001', 'E'), (1, 'c0001', 'B'), (4, 'c0001', 'C'), (7, 'c0002', 'G'), (9, 'c0072', 'E')]
        self.t.addDataToTimetable(assignedList)
        result = softConstraints2.softConstraintsPenalty(self.t.getTimeTable(), self.data, "perturbation")
        self.assertEqual(sum(map(lambda x: result['perturbationPenalty'][x], result['perturbationPenalty'])), 896)






