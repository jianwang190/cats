import math, random
from cats.utils.timetable import TimeTableFactory
from cats.adaptiveTabuSearch.softConstraints2 import totalSoftConstraintsForTimetable
from cats.ga.checkHardConstraints import countHardConstraints, checkHardConstraintsForSlots, countTeachersConflicts, \
    countCurriculumConflicts, countRoomOccupancy, countConstraintsList, countMissingLectures, countRoomTypeViolations
import time

#noinspection PyPep8Naming
class GeneticAlgorithmSchool(object):

    def __init__(self, data, timeout=3600):
        self.data = data
        self.fitnessTable = dict()
        self.populationSize = 200
        self.mutationIndex = 0.01
        self.tournamentSelectionIndex = 3
        self.fitnessSum = 0
        self.iterationsMax = 1000
        self.bestSolutionIndex = -1
        self.timeout = timeout
        self.startTime = time.time()
        self.fitnessOperations = 0
        self.f = 0
        self.f2 = 0
        self.timeTables = dict()

        self.generateInitialSolutions()
        self.estimateFitness()
        self.runAlgorithmLoop()

        self.saveBestTimeTableToFile("/home/filip/Inzynierka/cats/Plany/plan" + str(random.randint(0, 10000)) + ".txt")
        #self.printFinalOutput()


    def runAlgorithmLoop(self):
        for epoch in range(self.iterationsMax):
            self.nextGeneration("tournament")
            self.mutate()
            self.estimateFitness()
            #self.showSolutionStatus(epoch)
            hardy = countHardConstraints(self.timeTables[self.bestSolutionIndex], self.data)
            self.f.write(str(hardy) + "+" \
                         + str(self.fitnessTable[self.bestSolutionIndex] - hardy) + " " \
                         + str(self.fitnessOperations) + "\n")
            currentTime = time.time()
            self.f2.write(str(epoch) + " " + str(self.fitnessTable[self.bestSolutionIndex]) + " " + str(currentTime - self.startTime) + "\n")
            print epoch, self.fitnessTable[self.bestSolutionIndex], currentTime - self.startTime

            if int(currentTime - self.startTime) > self.timeout:
                print "Loops:", epoch, "Execution timeout after", currentTime - self.startTime
                self.f.close()
                self.f2.close()
                return

        self.f.close()
        self.f2.close()

        #print "Loops:", self.iterationsMax, "Score:", str(self.fitnessTable[self.bestSolutionIndex]), \
        #    "Execution time", currentTime - self.startTime

    def generateInitialSolutions(self):
        shuffledCourses = self.data.getAllCourseIds()
        for populationId in range(self.populationSize):
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
                self.assignMissingLectures(self.timeTables[populationId], courseId, unassignedLecturesNum)

        self.f = open("/home/filip/Inzynierka/cats/Plany/progres" + str(random.randint(0, 10000)) + ".txt", 'w')
        self.f2 = open("/home/filip/Inzynierka/cats/Plany/raport" + str(random.randint(0, 10000)) + ".txt", 'w')
        self.f.write("0+0 0\n")

    def chooseBestRoom(self, populationId, courseId):
        #roomList = self.timeTables[populationId].getRoomsIdForCourses(self.data.getAllRooms(),[self.data.getCourse(courseId)])[courseId]

        #Take MinWorkingDays into account
        #while len(roomList) > 0:
        #    bestRoom = self.data.getBestRoom(roomList)
        #    pairs = self.timeTables[populationId].availableSlotRoomPairs(self.data, courseId)
        #    pairs = filter(lambda x : bestRoom.id in x[1], pairs.iteritems())
        #    assignedDays = self.timeTables[populationId].getAssignedDays(courseId)
        #    if self.data.getCourse(courseId).minWorkingDays > len(assignedDays):
        #        pairs = filter(lambda x : self.timeTables[populationId].getPeriodPair(x[0])[0] not in assignedDays,\
        #                     pairs)
        #        if len(pairs) > 0:
        #            sortedPairs = sorted(pairs, key = lambda x : len(x[1]), reverse = True)
        #            return (sortedPairs[0][0], bestRoom.id)
        #        else:
        #            roomList.remove(bestRoom.id)
        #    else:
        #        break

        #Discard MinWorkingDays
        roomList = self.timeTables[populationId].getRoomsIdForCourses(self.data.getAllRooms(), \
                                                                      [self.data.getCourse(courseId)])[courseId]

        while len(roomList) > 0:
            bestRoom = self.data.getBestRoom(roomList)
            pairs = self.timeTables[populationId].availableSlotRoomPairs(self.data, courseId)
            pairs = filter(lambda x : bestRoom.id in x[1], pairs.iteritems())
            if len(pairs) > 0:
                sortedPairs = sorted(pairs, key = lambda x : len(x[1]), reverse = True)
                return (sortedPairs[0][0], bestRoom.id)
            roomList.remove(bestRoom.id)

        return ()

    def assignMissingLectures(self, solution, courseId, amount):
        if amount <= 0:
            return
        timeSlots = solution.timeSlots
        for i in range(amount):
            tries = 0
            random.shuffle(timeSlots)
            roomID = -1
            for slot in timeSlots:
                tries += 1
                freeRoomsIDs = solution.availableRoomsList(slot, self.data, courseId)
                if len(freeRoomsIDs) > 0:
                    if slot in solution.availableSlotsForCourse(self.data, courseId):
                        #Discard the room capacity, consider room type, constraints and curriculums
                        roomID = max(freeRoomsIDs, key = lambda x : self.data.getRoom(x).capacity)
                        break
            if roomID == -1:
                for slot in timeSlots:
                    #Discard the constraints list, consider curriculum conflicts and room type
                    tries += 1
                    banned = False
                    freeRoomsIDs = solution.availableRoomsList(slot, self.data, courseId)
                    if len(freeRoomsIDs) > 0:
                        for lecture in solution.getTimeTable()[slot]:
                            if lecture[0] in solution.neighbourhoodList[courseId]:
                                banned = True
                                break
                        if not banned:
                            roomID = max(freeRoomsIDs, key = lambda x : self.data.getRoom(x).capacity)
                            break
            if roomID == -1:
                for slot in timeSlots:
                    #Discard the curriculum conflicts, consider constraints and room type
                    tries += 1
                    banned = False
                    freeRoomsIDs = solution.availableRoomsList(slot, self.data, courseId)
                    if len(freeRoomsIDs) > 0:
                        for constraint in self.data.getConstraintsForCourse(courseId):
                            if constraint.day == solution.getPeriodPair(slot)[0] and \
                                            constraint.dayPeriod == solution.getPeriodPair(slot)[1]:
                                banned = True
                                break
                        if not banned:
                            roomID = max(freeRoomsIDs, key = lambda x : self.data.getRoom(x).capacity)
                            break
            if roomID == -1:
                for slot in timeSlots:
                    #Discard constraints and curriculum conflicts, consider room type
                    tries += 1
                    freeRoomsIDs = solution.availableRoomsList(slot, self.data, courseId)
                    if len(freeRoomsIDs) > 0:
                        roomID = max(freeRoomsIDs, key = lambda x : self.data.getRoom(x).capacity)
                        break

            if roomID == -1:
                for slot in timeSlots:
                    #Discard constraints, curriculum conflicts and room type
                    tries += 1
                    freeRoomsIDs = solution.allAvailableRoomsList(slot, self.data)
                    if len(freeRoomsIDs) > 0:
                        roomID = max(freeRoomsIDs, key = lambda x : self.data.getRoom(x).capacity)
                        break

            solution.addDataToTimetable([(slot, courseId, roomID)])


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

        self.timeTables = self.selectSurvivals(self.timeTables, newGeneration)

    def selectSurvivals(self, parents, children):
        # Let the better half of parents and children survive the current generation
        newGeneration = dict()
        sortedParents = sorted(parents.iteritems(), key = lambda x : self.fitnessTable[x[0]])
        sortedChildren = sorted(children.iteritems(), key = lambda x : self.fitnessTable[x[0]])
        for i in range(self.populationSize):
            if i%2 == 0:
                newGeneration[i] = sortedParents[i/2][1]
            else:
                newGeneration[i] = sortedChildren[i/2][1]

        return newGeneration

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

        self.fitnessSum = fitnesSum
        self.fitnessOperations += self.populationSize
        self.bestSolutionIndex = self.getTopSolutionIndex()

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
        :return:new pair of children
        """
        courses = self.data.getAllCourseIds()
        random.shuffle(courses)
        child1 = self.createChild(mother, father, courses)
        child2 = self.createChild(father, mother, courses)

        return (child1, child2)

    def createChild(self, mother, father, courseIds):

        child = mother.copySolution(self.data)
        insertedLectures = 0
        allLecturesCount = self.data.getAllLecturesCount()

        for courseId in courseIds:
            lectures1 = father.assignedLecturesWithSlots(courseId)
            for slotItem in lectures1:
                for lecture in slotItem[1]:
                    if not self.insertGeneWithHardCheck(slotItem[0], lecture, child):
                        continue
                    insertedLectures += 1
                    if insertedLectures >= allLecturesCount/2:
                        return child

        """
        for courseId in courseIds:
            lectures1 = father.assignedLecturesWithSlots(courseId)
            for slotItem in lectures1:
                for lecture in slotItem[1]:
                    if not self.geneticRepair(slotItem[0], lecture, child):
                        continue
                    insertedLectures += 1
                    if insertedLectures >= allLecturesCount/2:
                        return child
        """
        return child

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
        """"
        #Look for any valid room in another time slot
        for period in periods:
            rooms = solution.availableRoomsForCourseAndSlot(self.data, lecture[0], period)
            rooms = sorted(rooms, key = lambda x : self.data.getRoom(x).capacity)
            for roomId in rooms:
                if solution.checkIfInsertionIsValid(period, lecture[0], roomId, self.data):
                    return True
                else:
                    solution.removeFromTimetable([(period, lecture[0], roomId)])
        """
        return False


    def updateMutationIndex(self):
        if self.mutationIndex > 0.5:
                self.mutationIndex = 0.5
        else:
            if self.mutationIndex < 0.5:
                self.mutationIndex *= 1.02

    def mutate(self):
        """
        Mutation make a swap in a timetable between 2 random lectures only if it doesn't make solution worse
        :param population:
        :param fitnessTable:
        :return:
        """
        self.updateMutationIndex()

        for i in range(int(math.ceil(self.mutationIndex * self.populationSize))):
            """ Prevent the top solution from a potential regression """
            solutionId = self.getTopSolutionIndex()
            while solutionId == self.getTopSolutionIndex():
                solutionId = random.choice(self.timeTables.keys())

            for i in range(1000):
                course1 = self.data.getRandomCourse()
                course2 = self.data.getRandomCourse()
                if course1.id != course2.id:
                    lecture1 = random.choice(self.timeTables[solutionId].assignedLecturesWithSlots(course1.id))
                    lecture2 = random.choice(self.timeTables[solutionId].assignedLecturesWithSlots(course2.id))
                    if self.swapGenesWithHardCheck(lecture1[0], lecture1[1][0], lecture2[0], lecture2[1][0],\
                                                   self.timeTables[solutionId]):
                        return
                    else:
                        self.rollBackSwap(lecture1[0], lecture1[1][0], lecture2[0], lecture2[1][0],\
                                                   self.timeTables[solutionId])

    def swapGenes(self, slot1, gene1, slot2, gene2, solution):
        solution.getTimeTable()[slot2].remove(gene2)
        solution.getTimeTable()[slot1].remove(gene1)
        solution.getTimeTable()[slot2].append((gene1[0], gene2[1]))
        solution.getTimeTable()[slot1].append((gene2[0], gene1[1]))

    def rollBackSwap(self, slot1, gene1, slot2, gene2, solution):
        solution.getTimeTable()[slot2].remove((gene1[0], gene2[1]))
        solution.getTimeTable()[slot1].remove((gene2[0], gene1[1]))
        solution.getTimeTable()[slot2].append(gene2)
        solution.getTimeTable()[slot1].append(gene1)

    def swapGenesWithHardCheck(self, slot1, gene1, slot2, gene2, solution):
        initialPenalty = checkHardConstraintsForSlots(solution, self.data, (slot1, slot2))
        self.swapGenes(slot1, gene1, slot2, gene2, solution)
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

        penalty = countCurriculumConflicts(self.timeTables[self.bestSolutionIndex], \
                                            self.timeTables[self.bestSolutionIndex].getTimeTable().keys(), self.data)
        print "Przedmioty w tym samym kurikulum", penalty
        penalty += countMissingLectures(self.timeTables[self.bestSolutionIndex], self.data)
        print "Brakujace zajecia", penalty
        penalty += countRoomOccupancy(self.timeTables[self.bestSolutionIndex],
                                      self.timeTables[self.bestSolutionIndex].getTimeTable().keys())
        print "Dwa zajecia w tej samej sali", penalty
        penalty += countConstraintsList(self.timeTables[self.bestSolutionIndex], \
                                        self.timeTables[self.bestSolutionIndex].getTimeTable().keys(), self.data)
        print "Lista constraintow", penalty
        penalty += countTeachersConflicts(self.timeTables[self.bestSolutionIndex], \
                                          self.timeTables[self.bestSolutionIndex].getTimeTable().keys(), self.data)
        print "Nauczyciel ma 2 kursy na raz", penalty
        penalty += countRoomTypeViolations(self.timeTables[self.bestSolutionIndex], \
                                          self.timeTables[self.bestSolutionIndex].getTimeTable().keys(), self.data)
        print "Typ sali", penalty

        hardConstraintsPenalty = countHardConstraints(self.timeTables[self.bestSolutionIndex], self.data)
        bestFitnessValue = self.fitnessTable[self.bestSolutionIndex]
        print "Epoka:", epoch, "Hardy:", str(hardConstraintsPenalty), \
            "Softy:", str(bestFitnessValue-hardConstraintsPenalty), "najlepszy wynik:", str(bestFitnessValue)

    def printFinalOutput(self):
        bestSolutionId = self.getTopSolutionIndex()
        for slot in self.timeTables[bestSolutionId].getTimeTable().keys():
            for lecture in self.timeTables[bestSolutionId].getTimeTable()[slot]:
                line = lecture[0] + ' ' + lecture[1] + ' ' + str(self.timeTables[bestSolutionId].getPeriodPair(slot)[0])\
                       + ' ' + str(self.timeTables[bestSolutionId].getPeriodPair(slot)[1])
                print line
