import random
from copy import deepcopy

class Particle(object):
    """Store actual and best solution of particle"""

    def __init__(self, timetable, timetableFactory):
        self.actualSolution = timetable
        self.bestSolution = None
        self.timetableFactory = timetableFactory

    def updateLocalBestSolution(self):
        """Update local Best"""

        if self.bestSolution == None or self.actualSolution.penalty < self.bestSolution.penalty:
            self.bestSolution = deepcopy(self.actualSolution)

    def produceNewSolution(self, globalBest):
        """Produce new solution"""

        #self.actualSolution = deepcopy(globalBest)
        #for x in range(10):
            #self.randChange(self.bestSolution)
        #for x in range(100):
            #self.randChange(globalBest)

        #self.randSelfChange()

        self.randSelfChange()
        self.randChange(self.bestSolution)
        self.randChange(globalBest)

    def randSelfChange(self):
        """Change randomly two courses in actualSolution"""
        slot1 = self.timetableFactory.getRandomSlot()
        slot2 = self.timetableFactory.getRandomSlot()

        self.swapCourses(slot1, slot2)

    def randChange(self, timetable):
        """Change randomly one courseId from actualSolution and timetable"""

        slot1 = self.timetableFactory.getRandomSlot()
        day1, period1, room1 = self.timetableFactory.unzip(slot1)

        course = timetable.periods[day1][period1][room1.id]

        if course is None:
            slot2 = self.timetableFactory.getRandomSlot()
        else:
            slot2 = random.sample(self.actualSolution.courses[course.id], 1)[0]

        self.swapCourses(slot1, slot2)

    def swapCourses(self, slot1, slot2):
        """Swap two courses in actualSolution"""

        day1, period1, room1 = self.timetableFactory.unzip(slot1)
        day2, period2, room2 = self.timetableFactory.unzip(slot2)

        course1 = self.actualSolution.periods[day1][period1][room1.id]
        course2 = self.actualSolution.periods[day2][period2][room2.id]

        if course1 != None and course2 != None and course1.id == course2.id:
            return

        if course1 != None:
            self.actualSolution.courses[course1.id].remove(slot1)
            self.actualSolution.courses[course1.id].add(slot2)

        if course2 != None:
            self.actualSolution.courses[course2.id].remove(slot2)
            self.actualSolution.courses[course2.id].add(slot1)

        self.actualSolution.periods[day1][period1][room1.id], \
        self.actualSolution.periods[day2][period2][room2.id] = \
        self.actualSolution.periods[day2][period2][room2.id], \
        self.actualSolution.periods[day1][period1][room1.id]

