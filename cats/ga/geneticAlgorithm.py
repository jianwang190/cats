import itertools
import random
from cats.utils.data import Data
from cats.utils.timetable import TimeTable, CellOfTimeTable, TimeTableFactory

class GeneticAlgorithm(object):
    mutationIndex = 0.1
    tournamentSelectionIndex = 4

    def __init__(self, data):
        self.data = data
        self.timeTable = TimeTableFactory.getTimeTable(data)

    def generateInitialSolution(self):
        for course in self.data.courses:
            # promote early classes - random.paretovariate
            periods = self.timeTable.availablePeriodsRooms(self.data.constraints, course.id)
            slot = random.randint(0, periods['availablePairsNum']-1)
            print course.id
            for room in periods['availablePairs'][slot]:
                print room
            roomId = random.sample(periods['availablePairs'][slot], 1)
            #curId = self.timeTable.getCurriculumOfCourse(self.data.curricula, course.id)
            #self.timeTable.addDataToTimetable(slot, course.id, periods['availablePairs'][slot][roomId], curId)
            self.timeTable.addDataToTimetable([(slot, course.id, roomId[0])])

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