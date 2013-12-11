class DictData():
    """
    Structure containing data

    """
    courses = {}
    rooms = {}
    curricula = {}
    constraints = {}

    curriculumLookup = {}


    def getAllCourses(self):
        """
        Get all courses

        rtype : object
        """
        return self.courses.values()
    def getAllRooms(self):
        """
        Get all rooms

        :return:
        """
        return self.rooms.values()
    def getAllCurricula(self):
        """
        Get all curricula

        :return:
        """
        return self.curricula.values()
    def getAllConstraints(self):
        return sum(self.constraints.values(),[])



    def getCourse(self, id):
        """
        Get Course

        :param id:
        :return:
        """
        return self.courses[id]
    def getRoom(self, id):
        """
        Get room

        :param id:
        :return:
        """
        return self.rooms[id]
    def getCurriculum(self, id):
        """
        Get curriculum

        :param id:
        :return:
        """
        return self.curricula[id]
    def getConstraintsForCourse(self, id):
        """
        Get constraints for course

        :param id:
        :return:
        """
        return self.constraints[id]

    def getMembersCurriculum(self, id):
        """
        Get members curriculum

        :param id:
        :return:
        """
        return self.curricula[id].members

