import random
from copy import deepcopy

class Timetable(object):
    """Store timetable"""

    def __init__(self, data):
        rooms = data.rooms
        daysNum = data.daysNum
        periodsPerDay = data.periodsPerDay
        courses = data.courses

        idList = [room.id for room in rooms]
        noneList = [None for i in range(len(rooms))]
        roomsDict = dict(zip(idList, noneList))
        self.periods = [[deepcopy(roomsDict) for j in range(periodsPerDay)] for i in range(daysNum)]

        idList = [course.id for course in courses]
        tmpList = [set() for i in range(len(courses))]
        self.courses = dict(zip(idList, tmpList))

        self.penalty = None



class TimetableFactory(object):
    """Create timetables"""

    def __init__(self, data):
        self.data = data

    def getEmptyTimetable(self):
        """Return empty timetable"""

        return Timetable(self.data)

    def getRandomTimetable(self):
        """Return random timetable"""

        timetable = self.getEmptyTimetable()

        slots = range(self.data.daysNum * self.data.periodsPerDay * len(self.data.rooms))
        random.shuffle(slots)

        for course in self.data.courses:
            for lecture in range(course.lectureNum):
                slot = slots.pop()
                day, period, room = self.unzip(slot)
                timetable.periods[day][period][room.id] = course
                timetable.courses[course.id].add(slot)

        return timetable

    def getRandomSlot(self):
        """Return random slot"""

        slot = random.randint(0, self.data.daysNum * self.data.periodsPerDay * len(self.data.rooms) - 1)

        return slot

    def unzip(self, slot):
        """Unzip day, period and room from slot"""

        day = slot / (self.data.periodsPerDay * len(self.data.rooms))
        slot -= day * (self.data.periodsPerDay * len(self.data.rooms))
        period = slot / len(self.data.rooms)
        slot -= period * len(self.data.rooms)
        roomNr = slot
        room = self.data.rooms[roomNr]

        return day, period, room

    def echo(self, timetable):
        """Printe timetable"""

        for day in range(len(timetable.periods)):
            for period in range(len(timetable.periods[day])):
                for room in timetable.periods[day][period]:
                    course = timetable.periods[day][period][room]
                    if course != None:
                        print day * self.data.periodsPerDay + period , course.id, room
