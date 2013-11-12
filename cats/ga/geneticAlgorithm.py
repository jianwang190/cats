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

    def generateInitialSolutions(self):
        for populationId in range(self.populationSize):
            for course in self.data.courses:
                # promote early classes - random.paretovariate
                periods = self.timeTables[populationId].availablePeriodsRooms(self.data.constraints, course.id)
                slots = random.sample(periods['availablePairs'].keys(), course.lectureNum)
                assignedList = list()
                for slot in slots:
                    assignedList.append([slot, course.id, periods['availablePairs'][slot]])
                self.TimeTables[populationId].addDataToTimetable(assignedList)

        return self.timeTables

    def nextGeneration(self, population, selectionMethod):
        newGeneration = dict()
        for i in range(len(population)):
            if selectionMethod == "tournament":
                parents = self.tournamentSelect(population)
            elif selectionMethod == "roulette":
                parents = self.rouletteSelect(population)
            elif selectionMethod == "random":
                parents = self.randomSelect(population)
            else:
                raise Exception("Wrong selection method pointed!")
            child = self.Crossing(parents[0], parents[1], i)
            newGeneration[i] = child

        return newGeneration

    def estimateFitness(self, population):
        fitnessTable = dict()
        for solutionId in population.keys():
            fitnessTable[solutionId] = self.fitness(self.timeTables[solutionId])

        return fitnessTable

    def fitness(self, solution):
        return random.randint(20, 200)

    def getTopSolution(self, solutionsFitness):
        return min(solutionsFitness.iterkeys(), key=lambda k: solutionsFitness[k])

    def Crossing(self, mother, father, Id):
        child = dict()
        #genes sorted by courseID
        sortedMother = sorted(mother.items(), key = lambda x : x[1]['courseId'])
        sortedFather = sorted(father.items(), key = lambda x : x[1]['courseId'])
        #get from mother courses with even id number
        for item in sortedMother:
            if (int(item[1]['courseId'])%2 == 0):
                child[item[0]].append(CellOfTimeTable(item[1]['courseId'],item[1]['roomId']))
        #get from father courses with odd id number
        for item in sortedFather:
            if (int(item[1]['courseId'])%2 == 1):
                child[item[0]].append(CellOfTimeTable(item[1]['courseId'],item[1]['roomId']))

        return child

    def mutate(self, population):
        for i in math.ceil(self.mutationIndex / len(population)):
            solutionId = random.choice(len(population) - 1)
            course = random.choice(self.data.courses)
            # delete whole old schedule of the course

            periods = population[solutionId].availablePeriodsRooms(self.data.constraints, course.id)
            slots = random.sample(periods['availablePairs'].keys(), course.lectureNum)
            assignedList = list()
            for slot in slots:
                assignedList.append([slot, course.id, periods['availablePairs'][slot]])
            population[solutionId].addDataToTimetable(assignedList)

        return population


    def tournamentSelect(self, population):
        parent1 = random.choice(population)
        parent2 = random.choice(population)

        return [parent1, parent2]

    def rouletteSelect(self, population):
        parent1 = random.choice(population)
        parent2 = random.choice(population)

        return [parent1, parent2]


    def randomSelect(self, population):
        parent1 = random.choice(population)
        parent2 = random.choice(population)

        return [parent1, parent2]