import itertools, math, random
from cats.utils.data import Data
from cats.utils.timetable import TimeTable, TimeTableFactory
from cats.adaptiveTabuSearch.softConstraints2 import totalSoftConstraintsForTimetable
from cats.adaptiveTabuSearch.heuristics import initialSolutionWithReturn

class GeneticAlgorithm(object):

    def __init__(self, data, timeTables, populationSize = 100, mutationIndex = 0.01, tournamentSelcetionIndex = 4, iterations = 100):
        self.data = data
        self.timeTables = timeTables
        self.fitnessTable = dict()
        self.populationSize = populationSize
        self.mutationIndex = mutationIndex
        self.tournamentSelectionIndex = tournamentSelcetionIndex
        self.fitnessSum = 0
        self.iterationsMax = iterations

    def generateInitialSolutions(self):
        """Courses sorted by the amount o students attending"""
        sortedCourses = sorted(self.data.courses.values(), key = lambda course : course.studentsNum, reverse=True)
        for populationId in range(self.populationSize):
            self.timeTables[populationId] = TimeTableFactory.getTimeTable(self.data)
            for course in sortedCourses:
                # promote early classes - random.paretovariate
                pairs = self.timeTables[populationId].availableSlotRoomPairs(self.data, course.id)
                sortedPairs = sorted(pairs.iteritems(), key = lambda x : len(x[1]))
                print "pary, lectureNum, courseId : ", len(pairs.keys()),\
                    self.data.getCourse(course.id).lectureNum, course.id
                #slots = random.sample(pairs.keys(), self.data.getCourse(course.id).lectureNum)
                if self.data.getCourse(course.id).lectureNum > len(sortedPairs):
                    print "Bedzie brakowac zajec!"
                slots = sortedPairs[:self.data.getCourse(course.id).lectureNum]
                assignedList = list()
                for slot in slots:
                    assignedList.append((slot[0], course.id, self.data.getBestRoom(slot[1]).id))
                self.timeTables[populationId].addDataToTimetable(assignedList)

        return self.timeTables

    def generateFirstSolutions(self, solutions):
        self.sortedRoomIdList = sorted(self.data.getAllRooms(), key=lambda room: room.capacity, reverse=True)
        for populationId in range(len(solutions)):
            self.data.clearAssignedLectures(self.data.getAllCourses())
            self.timeTables[populationId] = initialSolutionWithReturn(solutions[populationId], self.data)

        return self.timeTables

    def nextGeneration(self, population, fitnessTable, selectionMethod):
        newGeneration = dict()
        for i in range(len(population)):
            if selectionMethod == "tournament":
                parents = self.tournamentSelect(population, fitnessTable)
            elif selectionMethod == "roulette":
                parents = self.rouletteSelect(population, fitnessTable)
            elif selectionMethod == "random":
                parents = self.randomSelect(population)
            else:
                raise Exception("Wrong selection method pointed!")
            child = self.Crossing(parents[0], parents[1])
            newGeneration[i] = child

        """Dorzucic wybieranie najlepszych z dzieci i rodzicow naraz"""
        return newGeneration

    def estimateFitness(self, population):
        fitnessTable = dict()
        fitnesSum = 0.0
        for solutionId in population.keys():
            fitnessTable[solutionId] = self.fitness(self.timeTables[solutionId])
            fitnesSum += (1000/fitnessTable[solutionId])

        self.fitnessSum = fitnesSum
        return fitnessTable

    def fitness(self, solution):
        return totalSoftConstraintsForTimetable(solution.getTimeTable(), self.data)

    def getTopSolution(self, solutionsFitness):
        return min(solutionsFitness.iterkeys(), key=lambda k: solutionsFitness[k])

    def Crossing(self, mother, father):
        child = TimeTableFactory.getTimeTable(self.data)

        for courseId in self.data.courses.keys():
            if int(courseId[1:]) % 2 == 0:
                lectures = mother.assignedLectures(courseId)
            else:
                lectures = father.assignedLectures(courseId)
            assignedList = list()
            for slot in lectures.keys():
                for lecture in lectures[slot]:
                    assignedList.append((slot, lecture[0], lecture[1]))
            child.addDataToTimetable(assignedList)

        return child

    def mutate(self, population, fitnessTable):
        for i in range(int(math.ceil(self.mutationIndex * len(population)))):
            """
                Prevent the top solution from a potential regression
            """
            while True:
                solutionId = random.randint(0, len(population)-1)
                if int(fitnessTable[solutionId]) < int(fitnessTable[self.getTopSolution(fitnessTable)]):
                    break
            course = self.data.getRandomCourse()
            # delete whole old schedule of the course
            for slot, cells in population[solutionId].timeTable.iteritems():
                for schedule in cells:
                    if schedule[0] == course.id:
                        population[solutionId].timeTable[slot].remove(schedule)
            periods = population[solutionId].availablePeriodsRooms(self.data.constraints, course.id)
            slots = random.sample(periods['availablePairs'].keys(), course.lectureNum)
            assignedList = list()
            for slot in slots:
                assignedList.append((slot, course.id, periods['availablePairs'][slot]))
            population[solutionId].addDataToTimetable(assignedList)

        return population


    def tournamentSelect(self, population, fitnessTable):
        while True:
            parent1 = self.getTournamentParentIndex(len(population), fitnessTable)
            parent2 = self.getTournamentParentIndex(len(population), fitnessTable)
            if int(parent1) != int(parent2):
                break

        return [population[parent1], population[parent2]]

    def rouletteSelect(self, population, fitnessTable):
        while True:
            parent1 = self.getRouletteIndex(fitnessTable)
            parent2 = self.getRouletteIndex(fitnessTable)
            if int(parent1) != int(parent2):
                break

        return [population[parent1], population[parent2]]


    def randomSelect(self, population):
        while True:
            parent1 = random.choice(population.keys())
            parent2 = random.choice(population.keys())
            if int(parent1) != int(parent2):
                break

        return [population[parent1], population[parent2]]

    def getRouletteIndex(self, fitnessTable):
        rouletteValue = random.randint(0, self.fitnessSum)
        index = 0
        tempValue = 0
        while(tempValue < rouletteValue):
            tempValue += (1000/fitnessTable[index])
            index+=1

        return index-1

    def getTournamentParentIndex(self, populationSize, fitnessTable):
        candidates = [self.tournamentSelectionIndex]
        for i in range(self.tournamentSelectionIndex):
            candidates[i] = random.randint(0, populationSize)

        return min(candidates, key = lambda k: fitnessTable[k])