import os

from inputDataStructures import Course, Room, Curriculum, Constraint
from data import Data


class CompetitionReader(object):
    """Read data from file"""

    def __init__(self):
        self.data = Data()
        self.buffer = []

    def readInstance(self, instanceNr):
        """Return data object with data from instance file"""


        self.buffer = self.readFile(instanceNr)

        self.getHeader()
        self.getCourses()
        self.getRooms()
        self.getCurricula()
        self.getConstraints()

        return self.data

    def readFile(self, instanceNr):
        """Return content of file"""

        path = u"data/Curriculum_based_Course_timetabling/datasets/comp" + str(instanceNr) + ".ctt"
        f = open(path, "r")
        content = map(lambda x: x.rstrip('\n'), f.readlines())

        return content

    def getHeader(self):
        """Get header from buffer"""

        self.data.instanceName = self.buffer[0].strip('Name: ')
        self.data.daysNum = int(self.buffer[3].strip('Days: '))
        self.data.periods_per_day = int(self.buffer[4].strip('Periods_per_day: '))

    def getCourses(self):
        """Get courses from buffer"""

        index = self.buffer.index('COURSES:') + 1

        while self.buffer[index] != '':
            s = self.buffer[index].split()
            course = Course(s[0], s[1], int(s[2]), int(s[3]), int(s[4]))
            self.data.courses.append(course)

            index += 1

    def getRooms(self):
        """Get rooms from buffer"""

        index = self.buffer.index('ROOMS:') + 1

        while self.buffer[index] != '':
            s = self.buffer[index].split()
            room = Room(s[0], int(s[1]))
            self.data.rooms.append(room)

            index += 1

    def getCurricula(self):
        """Get curricula from buffer"""

        index = self.buffer.index('CURRICULA:') + 1

        while self.buffer[index] != '':
            s = self.buffer[index].split()
            print s
            curriculum = Curriculum(s[0], int(s[1]), s[2:])
            self.data.curricula.append(curriculum)

            index += 1

    def getConstraints(self):
        """Get constraints from buffer"""

        index = self.buffer.index('UNAVAILABILITY_CONSTRAINTS:') + 1

        while self.buffer[index] != '':
            s = self.buffer[index].split()
            constraint = Constraint(s[0], int(s[1]), int(s[2]))
            self.data.constraints.append(constraint)

            index += 1





