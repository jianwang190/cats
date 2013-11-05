import itertools
from random import randint, random
from cats.utils.data import Data
from cats.utils.timetable import TimeTable, CellOfTimeTable, TimeTableFactory

class GeneticAlgorithm(object):
    mutationIndex = 0.1
    tournamentSelectionIndex = 4

    def __init__(self, data):
        self.data = data
        self.timeTable = TimeTableFactory.getTimeTable(data)

    def generateInitialSolution(self):
        for courseId in self.data.courses:
            # promote early classes - random.paretovariate
            periods = self.timeTable.availablePeriodsRooms(self.timeTable.getKeyConstraintsOfCourse(self.data.constraints, courseId), courseId)
            slot = random.randint(periods['availablePairsNum'])
            roomId = random.randint(periods['availablePairsNum'][slot])
            curId = self.timeTable.getCurriculumOfCourse(courseId)
            self.timeTable.addDataToTimetable(slot, courseId, roomId, curId)

    def doMutation(self):
        pass

    def doCrossover(self):
        pass

    def tournamentSelection(self):
        pass

    def rouletteSelection(self):
        pass

    def randomSelection(self):
        pass