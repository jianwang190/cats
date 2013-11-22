import itertools, math, random
from cats.utils.data import Data
from cats.utils.inputDataStructures import *
from cats.utils.timetable import TimeTable, TimeTableFactory
from cats.adaptiveTabuSearch.softConstraints2 import totalSoftConstraintsForTimetable
from cats.adaptiveTabuSearch.heuristics import initialSolutionWithReturn
from cats.ga.checkHardConstraints import countHardConstraints, checkHardConstraintsForSlots

#noinspection PyPep8Naming
class GeneticAlgorithm(object):

    def __init__(self, data, timeTables, populationSize = 100, mutationIndex = 0.01, \
                 tournamentSelectionIndex = 4, iterations = 100):
        self.data = data
        self.timeTables = timeTables
        self.fitnessTable = dict()
        self.populationSize = populationSize
        self.mutationIndex = mutationIndex
        self.tournamentSelectionIndex = tournamentSelectionIndex
        self.fitnessSum = 0
        self.iterationsMax = iterations


    def generateInitialSolutions(self):
        """Courses sorted by the amount o students attending"""
        #shuffledCourses = sorted(self.data.courses.values(), key = lambda course : course.studentsNum, reverse=True)
        for populationId in range(self.populationSize):
            shuffledCourses = self.data.getAllCourseIds()
            random.shuffle(shuffledCourses)
            self.timeTables[populationId] = TimeTableFactory.getTimeTable(self.data)
            for courseId in shuffledCourses:
                pairs = self.timeTables[populationId].availableSlotRoomPairs(self.data, courseId)
                sortedPairs = sorted(pairs.iteritems(), key = lambda x : len(x[1]))
                #slots = random.sample(pairs.keys(), self.data.getCourse(course.id).lectureNum)
                slots = sortedPairs[:self.data.getCourse(courseId).lectureNum]
                assignedList = list()
                for slot in slots:
                    assignedList.append((slot[0], courseId, self.data.getBestRoom(slot[1]).id))
                additionalList = self.timeTables[populationId].assignMissingLectures(self.data, courseId, \
                                                            (self.data.getCourse(courseId).lectureNum \
                                                             - len(sortedPairs)))
                self.timeTables[populationId].addDataToTimetable(assignedList)
                if len(additionalList) > 0:
                    if self.data.getCourse(courseId).lectureNum > (len(sortedPairs) + len(additionalList)):
                        print "Bedzie brakowac zajec!", courseId, self.data.getCourse(courseId).lectureNum -\
                                                        (len(sortedPairs) + len(additionalList))
                    self.timeTables[populationId].addDataToTimetable(additionalList)


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
            print "ID Fitness:", solutionId, self.fitnessTable[solutionId]

        self.fitnessSum = fitnesSum

    def fitness(self, solution):
        """
        Counts penalties for hard and soft constraints
        :param solution:
        :return: fitness value for solution
        """
        return countHardConstraints(solution, self.data) + \
               totalSoftConstraintsForTimetable(solution.getTimeTable(), self.data)

    def getTopSolution(self, solutionsFitness):
        """
        Returns a solution with minimal fitness value
        :param solutionsFitness:
        :return:
        """
        return min(solutionsFitness.iterkeys(), key=lambda k: solutionsFitness[k])

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
                for slot in lectures1.keys():
                    if insertedLectures < allLecturesCount/2:
                        for lecture in lectures1[slot]:
                            if not self.insertGeneWithHardCheck(slot, lecture, child1):
                                if not self.geneticRepair(slot, lecture, child1):
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
                for slot in lectures2.keys():
                    if insertedLectures < allLecturesCount/2:
                        for lecture in lectures2[slot]:
                            if not self.insertGeneWithHardCheck(slot, lecture, child2):
                                if not self.geneticRepair(slot, lecture, child2):
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
        if lecture != []:
            assignedLectures = filter(lambda x: x[1] != [], (solution.assignedLectures(lecture[0]).items()))
            lectureKeys = list()
            for item in assignedLectures:
                lectureKeys.append(item[0])
            if len(lectureKeys) == 0:
                pass
                #print "Blad"
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
                if int(self.fitnessTable[solutionId]) > int(self.fitnessTable[self.getTopSolution(self.fitnessTable)]):
                    break

            course = self.data.getRandomCourse()
            # delete whole old schedule of the course
            for slot, cells in self.timeTables[solutionId].timeTable.iteritems():
                for schedule in cells:
                    if schedule[0] == course.id:
                        self.timeTables[solutionId].timeTable[slot].remove(schedule)

            pairs = self.timeTables[solutionId].availableSlotRoomPairs(self.data, course.id)
            sortedPairs = sorted(pairs.iteritems(), key = lambda x : len(x[1]))
            #slots = random.sample(pairs.keys(), self.data.getCourse(course.id).lectureNum)
            slots = sortedPairs[:self.data.getCourse(course.id).lectureNum]
            assignedList = list()
            for slot in slots:
                assignedList.append((slot[0], course.id, self.data.getBestRoom(slot[1]).id))
            additionalList = self.timeTables[solutionId].assignMissingLectures(self.data, course.id, \
                                                            (self.data.getCourse(course.id).lectureNum \
                                                             - len(sortedPairs)))
            self.timeTables[solutionId].addDataToTimetable(assignedList)
            if len(additionalList) > 0:
                if self.data.getCourse(course.id).lectureNum > (len(sortedPairs) + len(additionalList)):
                    print "Bedzie brakowac zajec!", course.id, self.data.getCourse(course.id).lectureNum -\
                                                        (len(sortedPairs) + len(additionalList))
                    self.timeTables[solutionId].addDataToTimetable(additionalList)
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