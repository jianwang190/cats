import itertools, math, random
from cats.utils.data import Data
from cats.utils.inputDataStructures import *
from cats.utils.timetable import TimeTable, TimeTableFactory
from cats.adaptiveTabuSearch.softConstraints2 import totalSoftConstraintsForTimetable
from cats.adaptiveTabuSearch.heuristics import initialSolutionWithReturn
from cats.ga.checkHardConstraints import countHardConstraints, checkHardConstraintsForSlots
import time

#noinspection PyPep8Naming
class GeneticAlgorithm(object):

    def __init__(self, data, timeTables, populationSize = 100, iterations = 100, mutationIndex = 0.01, \
                 tournamentSelectionIndex = 4, timeout = 600):
        self.data = data
        self.timeTables = timeTables
        self.fitnessTable = dict()
        self.populationSize = populationSize
        self.mutationIndex = mutationIndex
        self.tournamentSelectionIndex = tournamentSelectionIndex
        self.fitnessSum = 0
        self.iterationsMax = iterations
        self.bestSolutionIndex = -1
        self.timeout = timeout
        self.startTime = time.time()


    def runAlgorithmLoop(self):
        for epoch in range(self.iterationsMax):
            self.nextGeneration("tournament")
            self.mutate()
            self.estimateFitness()
            self.showSolutionStatus(epoch)
            currentTime = time.time()
            if int(currentTime - self.startTime) > self.timeout:
                print "Loops:", epoch, "Execution timeout after", currentTime - self.startTime
                return

        print "Loops:", self.iterationsMax, "Execution time", currentTime - self.startTime

    def generateInitialSolutions(self):
        for populationId in range(self.populationSize):
            shuffledCourses = self.data.getAllCourseIds()
            random.shuffle(shuffledCourses)
            self.timeTables[populationId] = TimeTableFactory.getTimeTable(self.data)
            for courseId in shuffledCourses:
                unassignedLecturesNum = 0
                for i in range(self.data.getCourse(courseId).lectureNum):
                    slotRoomPair = self.chooseBestRoom(populationId, courseId)
                    if len(slotRoomPair) > 0:
                        self.timeTables[populationId].addDataToTimetable([(slotRoomPair[0], courseId, slotRoomPair[1])])
                    else:
                        unassignedLecturesNum += 1
                self.timeTables[populationId].assignMissingLectures(self.data, courseId, unassignedLecturesNum)


    def chooseBestRoom(self, populationId, courseId):
        pairs = dict()
        roomList = self.timeTables[populationId].getRoomsIdForCourses(self.data.getAllRooms(), \
                                                                      [self.data.getCourse(courseId)])[courseId]
        #Take MinWorkingDays into account
        while len(pairs) == 0:
            bestRoom = self.data.getBestRoom(roomList)
            pairs = self.timeTables[populationId].availableSlotRoomPairs(self.data, courseId)
            pairs = filter(lambda x : bestRoom.id in x[1], pairs.iteritems())
            assignedDays = self.timeTables[populationId].getAssignedDays(courseId)
            sortedPairs = sorted(pairs, key = lambda x : len(x[1]), reverse = True)
            index = 0
            if len(sortedPairs) > 0:
                if self.data.getCourse(courseId).minWorkingDays > len(set(assignedDays)):
                    while sortedPairs[index][0] in assignedDays:
                        index += 1
                        if index >= len(sortedPairs):
                            sortedPairs == list()
                            break
            roomList.remove(bestRoom.id)
            if len(roomList) == 0:
                break

        if len(sortedPairs) > 0:
            return (sortedPairs[index][0], bestRoom.id)
        #Discard MinWorkingDays
        roomList = self.timeTables[populationId].getRoomsIdForCourses(self.data.getAllRooms(), \
                                                                      [self.data.getCourse(courseId)])[courseId]
        pairs = dict()
        while len(pairs) == 0:
            bestRoom = self.data.getBestRoom(roomList)
            pairs = self.timeTables[populationId].availableSlotRoomPairs(self.data, courseId)
            pairs = filter(lambda x : bestRoom.id in x[1], pairs.iteritems())
            sortedPairs = sorted(pairs, key = lambda x : len(x[1]), reverse = True)
            roomList.remove(bestRoom.id)
            if len(roomList) == 0:
                return ()

        return (sortedPairs[0][0], bestRoom.id)

    def nextGeneration(self, selectionMethod):
        """

        :param population:
        :param fitnessTable:
        :param selectionMethod: "tournament" || "random" || "roulette"
        :return:
        """

        newGeneration = dict()
        for i in range(len(self.timeTables)/2):
            if selectionMethod == "tournament":
                parents = self.tournamentSelect(self.timeTables, self.fitnessTable)
            elif selectionMethod == "roulette":
                parents = self.rouletteSelect(self.timeTables, self.fitnessTable)
            elif selectionMethod == "random":
                parents = self.randomSelect(self.timeTables)
            else:
                raise Exception("Wrong selection method pointed!")
            children = self.crossover(parents[0], parents[1])
            newGeneration[i] = children[0]
            newGeneration[i+(len(self.timeTables)/2)] = children[1]

        """Dorzucic wybieranie najlepszych z dzieci i rodzicow naraz"""
        self.timeTables = newGeneration

    def estimateFitness(self):
        """
        Estimating fitness function for all individuals in population
        :param population:
        :return: dict { solutionId -> fitness[solution] }
        """

        fitnesSum = 0.0
        for solutionId in self.timeTables.keys():
            self.fitnessTable[solutionId] = self.fitness(self.timeTables[solutionId])
            fitnesSum += (1000/float(self.fitnessTable[solutionId]))
            #print "ID Fitness:", solutionId, self.fitnessTable[solutionId]

        self.fitnessSum = fitnesSum

    def fitness(self, solution):
        """
        Counts penalties for hard and soft constraints
        :param solution:
        :return: fitness value for solution
        """
        return countHardConstraints(solution, self.data) + \
               totalSoftConstraintsForTimetable(solution.getTimeTable(), self.data)

    def getTopSolutionIndex(self):
        """
        Returns a solution with minimal fitness value
        :param solutionsFitness:
        :return:
        """
        return min(self.fitnessTable.iterkeys(), key=lambda k: self.fitnessTable[k])

    def crossover(self, mother, father):
        """
        Perform a crossover over a given mother and father. Generate 2 children
        :param mother:
        :param father:
        :return:new child - the better one
        """
        child1 = mother.copySolution(self.data)
        child2 = father.copySolution(self.data)

        courses = self.data.getAllCourseIds()
        random.shuffle(courses)
        insertedLectures = 0
        allLecturesCount = self.data.getAllLecturesCount()
        for courseId in courses:
            lectures1 = father.assignedLectures(courseId)
            if insertedLectures < allLecturesCount/2:
                for slotItem in lectures1:
                    if insertedLectures < allLecturesCount/2:
                        for lecture in slotItem[1]:
                            if not self.insertGeneWithHardCheck(slotItem[0], lecture, child1):
                                if not self.geneticRepair(slotItem[0], lecture, child1):
                                    continue
                            insertedLectures += 1
                            if insertedLectures >= allLecturesCount/2:
                                break
                    else:
                        break
            else:
                break

        if insertedLectures < allLecturesCount/2:
            print "!!!!!!!!!!! Niepelny crossover dla child1 !!!!!!!!!!", \
                insertedLectures - (allLecturesCount/2)

        insertedLectures = 0
        for courseId in courses:
            lectures2 = mother.assignedLectures(courseId)
            if insertedLectures < allLecturesCount/2:
                for slotItem in lectures2:
                    if insertedLectures < allLecturesCount/2:
                        for lecture in slotItem[1]:
                            if not self.insertGeneWithHardCheck(slotItem[0], lecture, child2):
                                if not self.geneticRepair(slotItem[0], lecture, child2):
                                    continue
                            insertedLectures += 1
                            if insertedLectures >= allLecturesCount/2:
                                break
                    else:
                        break
            else:
                break

        if insertedLectures < allLecturesCount/2:
            print "!!!!!!!!!!! Niepelny crossover dla child2 !!!!!!!!!!", \
                insertedLectures - (allLecturesCount/2)

        return (child1, child2)


    def insertGeneWithHardCheck(self, slot, lecture, solution):
        #Checks if the lectures are identical
        for classs in solution.getTimeTable()[slot]:
            if lecture[1] == classs[1] and lecture[0] == classs[0]:
                return True

        #Checks if the room is already taken
        for classs in solution.getTimeTable()[slot]:
            if lecture[1] == classs[1]:
                return False

        #Checks if the penalty of solution arose after the gene insertion
        if solution.checkIfInsertionIsValid(slot, lecture[0], lecture[1], self.data):
            return True
        else:
            #Rollback the change
            solution.removeFromTimetable([(slot, lecture[0], lecture[1])])
            return False

    def geneticRepair(self, slot, lecture, solution):
        #If a gene to insert is not empty, delete its random equivalent at first
        if lecture != ():
            assignedLectures = solution.assignedLectures(lecture[0])
            lectureKeys = list()
            for item in assignedLectures:
                lectureKeys.append(item[0])
            else:
                chosenSlot = random.choice(lectureKeys)
                chosenRoom = solution.assignedLectures(lecture[0])[chosenSlot][0][1]
                assignedList = list()
                assignedList.append((chosenSlot, lecture[0], chosenRoom))
                solution.removeFromTimetable(assignedList)

        #Checks if the room is already taken
        roomTaken = False
        for classs in solution.getTimeTable()[slot]:
            if lecture[1] == classs[1]:
                roomTaken = True
                break

        #Try to insert gene in the same position
        if not roomTaken:
            if solution.checkIfInsertionIsValid(slot, lecture[0], lecture[1], self.data):
                return True
            else:
                solution.removeFromTimetable([(slot, lecture[0], lecture[1])])

        # Look for another slot with the same room to insert the gene
        periods = solution.timeSlots
        random.shuffle(periods)
        for period in periods:
            if solution.checkIfInsertionIsValid(period, lecture[0], lecture[1], self.data):
                return True
            else:
                solution.removeFromTimetable([(period, lecture[0], lecture[1])])

        #Look for any valid room in another time slot
        for period in periods:
            for roomId in solution.availableRoomsForCourseAndSlot(self.data, lecture[0], period):
                if solution.checkIfInsertionIsValid(period, lecture[0], roomId, self.data):
                    return True
                else:
                    solution.removeFromTimetable([(period, lecture[0], roomId)])

        return False


    def mutate(self):
        """
        Mutate
        :param population:
        :param fitnessTable:
        :return:
        """
        for i in range(int(math.ceil(self.mutationIndex * self.populationSize))):
            """ Prevent the top solution from a potential regression """
            while True:
                solutionId = random.choice(self.timeTables.keys())
                if solutionId != self.getTopSolutionIndex():
                    break

            course = self.data.getRandomCourse()
            # delete the whole old schedule of the course
            oldLectures = self.timeTables[solutionId].assignedLectures(course.id)
            self.timeTables[solutionId].removeFromTimetable(map(lambda x : (x[0], x[1][0], x[1][1]), oldLectures))

            unassignedLecturesNum = 0
            for i in range(self.data.getCourse(course.id).lectureNum):
                slotRoomPair = self.chooseBestRoom(solutionId, course.id)
                if len(slotRoomPair) > 0:
                    self.timeTables[solutionId].addDataToTimetable([(slotRoomPair[0], course.id, slotRoomPair[1])])
                else:
                    unassignedLecturesNum += 1
            self.timeTables[solutionId].assignMissingLectures(self.data, course.id, unassignedLecturesNum)
            """
            for i in range(self.populationSize * 100):
                slot1 = random.choice(self.timeTables[solutionId].getTimeTable().keys())
                roomId1 = (random.choice(self.data.getAllRooms())).id
                slot2 = random.choice(self.timeTables[solutionId].getTimeTable().keys())
                roomId2 = (random.choice(self.data.getAllRooms())).id
                if slot1 != slot2 and roomId1 != roomId2:
                    if self.swapGenesWithHardCheck(slot1, roomId1, slot2, roomId2, self.timeTables[solutionId]):
                        break
                    else: #roll back the changes with another swap
                        self.swapGenes(slot1, roomId1, slot2, roomId2, self.timeTables[solutionId])
            """


    def swapGenes(self, slot1, roomId1, slot2, roomId2, solution):
        #Default values "-1" if gene was not found
        lectures2 = solution.getTimeTable()[slot2]
        gene2 = next((x for x in lectures2 if x[1] == roomId2), ("-1", "-1"))

        lectures1 = solution.getTimeTable()[slot1]
        gene1 = next((x for x in lectures1 if x[1] == roomId1), ("-1", "-1"))

        if str(gene1[0]) == "-1" and str(gene2[0]) == "-1":
            return False

        if str(gene1[0]) != "-1" and str(gene2[0]) != "-1":
            solution.getTimeTable()[slot2].append(gene1)
            solution.getTimeTable()[slot1].append(gene2)
            solution.getTimeTable()[slot2].remove(gene2)
            solution.getTimeTable()[slot1].remove(gene1)
            return True

        if str(gene1[0]) == "-1":
            solution.getTimeTable()[slot1].append(gene2)
            solution.getTimeTable()[slot2].remove(gene2)
            return True

        if str(gene2[0]) == "-1":
            solution.getTimeTable()[slot2].append(gene1)
            solution.getTimeTable()[slot1].remove(gene1)
            return True

        return False


    def swapGenesWithHardCheck(self, slot1, roomId1, slot2, roomId2, solution):
        initialPenalty = checkHardConstraintsForSlots(solution, self.data, (slot1, slot2))
        if not self.swapGenes(slot1, roomId1, slot2, roomId2, solution):
            return False
        if initialPenalty >= checkHardConstraintsForSlots(solution, self.data, (slot1, slot2)):
            return True
        else:
            return False


    def tournamentSelect(self, population, fitnessTable):
        while True:
            parent1 = self.getTournamentParentIndex(len(population), fitnessTable)
            parent2 = self.getTournamentParentIndex(len(population), fitnessTable)
            if int(parent1) != int(parent2):
                break

        return (population[parent1], population[parent2])

    def rouletteSelect(self, population, fitnessTable):
        while True:
            parent1 = self.getRouletteIndex(fitnessTable)
            parent2 = self.getRouletteIndex(fitnessTable)
            if int(parent1) != int(parent2):
                break

        return (population[parent1], population[parent2])


    def randomSelect(self, population):
        while True:
            parent1 = random.choice(population.keys())
            parent2 = random.choice(population.keys())
            if int(parent1) != int(parent2):
                break

        return (population[parent1], population[parent2])

    def getRouletteIndex(self, fitnessTable):
        rouletteValue = random.random() * self.fitnessSum
        index = 0
        tempValue = 0.0
        while(tempValue < rouletteValue):
            tempValue += (1000/float(fitnessTable[index]))
            index += 1

        return index-1

    def getTournamentParentIndex(self, populationSize, fitnessTable):
        candidates = range(self.tournamentSelectionIndex)
        for i in range(self.tournamentSelectionIndex):
            candidates[i] = random.randint(0, populationSize-1)

        return min(candidates, key = lambda k: fitnessTable[k])

    def saveBestTimeTableToFile(self, fileName):
        bestSolutionId = self.getTopSolutionIndex()
        self.timeTables[bestSolutionId].saveResultsToFile(fileName)

    def showSolutionStatus(self, epoch):
        self.bestSolutionIndex = self.getTopSolutionIndex()
        hardConstraintsPenalty = countHardConstraints(self.timeTables[self.bestSolutionIndex], self.data)
        bestFitnessValue = self.fitnessTable[self.bestSolutionIndex]
        print "Epoka:", epoch, "Hardy:", str(hardConstraintsPenalty), \
            "Softy:", str(bestFitnessValue-hardConstraintsPenalty), "najlepszy wynik:", str(bestFitnessValue)