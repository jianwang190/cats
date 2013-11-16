import itertools, math, random
from cats.utils.data import Data
from cats.utils.timetable import TimeTable, CellOfTimeTable, TimeTableFactory

class GeneticAlgorithm(object):

    def __init__(self, data, timeTables, populationSize = 100, mutationIndex = 0.01, tournamentSelcetionIndex = 4):
        self.data = data
        self.timeTables = timeTables
        self.fitnessTable = dict()
        self.populationSize = populationSize
        self.mutationIndex = mutationIndex
        self.tournamentSelectionIndex = tournamentSelcetionIndex
        self.fitnessSum = 0

    def generateInitialSolutions(self):
        for populationId in range(self.populationSize):
            self.timeTables[populationId] = TimeTableFactory.getTimeTable(self.data)
            for course in self.data.courses:
                # promote early classes - random.paretovariate
                periods = self.timeTables[populationId].availablePeriodsRooms(self.data.constraints, course.id)
                slots = random.sample(periods['availablePairs'].keys(), course.lectureNum)
                assignedList = list()
                for slot in slots:
                    assignedList.append([slot, course.id, periods['availablePairs'][slot]])
                self.timeTables[populationId].addDataToTimetable(assignedList)

        return self.timeTables

    def nextGeneration(self, population, selectionMethod):
        newGeneration = dict()
        for i in range(len(population)):
            if selectionMethod == "tournament":
                parents = self.tournamentSelect(population, self.fitnessTable)
            elif selectionMethod == "roulette":
                parents = self.rouletteSelect(population, self.fitnessTable)
            elif selectionMethod == "random":
                parents = self.randomSelect(population)
            else:
                raise Exception("Wrong selection method pointed!")
            child = self.Crossing(parents[0], parents[1])
            newGeneration[i] = child

        return newGeneration

    def estimateFitness(self, population):
        fitnessTable = dict()
        fitnesSum = 0
        for solutionId in population.keys():
            fitnessTable[solutionId] = self.fitness(self.timeTables[solutionId])
            fitnesSum += fitnessTable[solutionId]

        self.fitnessSum = fitnesSum
        return fitnessTable

    def fitness(self, solution):
        return random.randint(20, 200)

    def getTopSolution(self, solutionsFitness):
        return min(solutionsFitness.iterkeys(), key=lambda k: solutionsFitness[k])

    def Crossing(self, mother, father):
        child = TimeTableFactory.getTimeTable(self.data)

        for course in self.data.courses:
            if int(course.id[1:]) % 2 == 0:
                lectures = mother.assignedLectures(course.id)
            else:
                lectures = father.assignedLectures(course.id)
            assignedList = list()
            for slot in lectures.keys():
                for lecture in lectures[slot]:
                    assignedList.append([slot, lecture.courseId, lecture.roomId])
            child.addDataToTimetable(assignedList)

        return child

    def mutate(self, population):
        for i in range(int(math.ceil(self.mutationIndex * len(population)))):
            solutionId = random.randint(0, len(population)-1)
            course = random.choice(self.data.courses)
            # delete whole old schedule of the course
            for slot, cells in population[solutionId].timeTable.iteritems():
                for schedule in cells:
                    if schedule.courseId == course.id:
                        population[solutionId].timeTable[slot].remove(schedule)
            periods = population[solutionId].availablePeriodsRooms(self.data.constraints, course.id)
            slots = random.sample(periods['availablePairs'].keys(), course.lectureNum)
            assignedList = list()
            for slot in slots:
                assignedList.append([slot, course.id, periods['availablePairs'][slot]])
            population[solutionId].addDataToTimetable(assignedList)

        return population


    def tournamentSelect(self, population, fitnessTable):
        parent1 = population[self.getTournamentParentIndex(len(population), fitnessTable)]
        parent2 = population[self.getTournamentParentIndex(len(population), fitnessTable)]

        return [parent1, parent2]

    def rouletteSelect(self, population, fitnessTable):
        parent1 = population[self.getRouletteIndex(fitnessTable)]
        parent2 = population[self.getRouletteIndex(fitnessTable)]

        return [parent1, parent2]


    def randomSelect(self, population):
        parent1 = random.choice(population)
        parent2 = random.choice(population)

        return [parent1, parent2]

    def getRouletteIndex(self, fitnessTable):
        rouletteValue = random.randint(0, self.fitnessSum)
        index = 0
        tempValue = 0
        while(tempValue < rouletteValue):
            tempValue += fitnessTable[index]
            index+=1

        return index-1

    def getTournamentParentIndex(self, populationSize, fitnessTable):
        candidates = [self.tournamentSelectionIndex]
        for i in range(self.tournamentSelectionIndex):
            candidates[i] = random.randint(0, populationSize)

        return max(candidates, key = lambda k: fitnessTable[k])