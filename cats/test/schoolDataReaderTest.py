__author__ = 'filip'
from cats.readers.competitionReader import CompetitionDictReader
import random

class LittleTest(object):
    def __init__(self):
        self.c = CompetitionDictReader()
        self.data = self.c.readInstance(22)

    def Run(self):
        #for course in self.data.getAllCourses():
        #    print "Course", course.id, course.typeOfRoom

        for i in range(10):
            courseId = random.choice(self.data.getAllCourseIds())
            print "C.id", courseId
            rooms = filter(lambda x : x.type == self.data.getCourse(courseId).typeOfRoom, self.data.getAllRooms())
            for room in rooms:
                print room.id, room.type

if __name__=="__main__":
    t=LittleTest()
    t.Run()
