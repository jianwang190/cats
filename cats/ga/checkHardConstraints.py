__author__ = 'filip'

def countHardConstraints(solution, data):

    """
    Counts the whole penalty for hard constraints in the entire timetable

    :param solution: the chosen timetable
    :param data: whole specification of constraints and regulations
    :return: total number of violations * 1000000
    """
    penalty = countCurriculumConflicts(solution, solution.getTimeTable().keys(), data)
    penalty += countMissingLectures(solution, data)
    penalty += countRoomOccupancy(solution, solution.getTimeTable().keys())
    penalty += countConstraintsList(solution, solution.getTimeTable().keys(), data)
    penalty += countTeachersConflicts(solution, solution.getTimeTable().keys(), data)
    penalty += countRoomTypeViolations(solution, solution.getTimeTable().keys(), data)

    return penalty

def checkHardConstraintsForSlots(solution, data, slots):
    """
    Counts the whole penalty for hard constraints for the given slots in timetable

    :param solution: timetable
    :param data: whole specification of constraints and regulations
    :param slots:
    :return: total number of violations * 1000000
    """
    penalty = countCurriculumConflicts(solution, slots, data)
    penalty += countRoomOccupancy(solution, slots)
    penalty += countConstraintsList(solution, slots, data)
    penalty += countTeachersConflicts(solution, slots, data)
    penalty += countRoomTypeViolations(solution, slots, data)

    return penalty

def countMissingLectures(solution, data):
    """
    Count the penalty for lectures which haven't been assigned

    :param solution: timetable object
    :param data: whole specification of constraints and regulations
    :return: number of violations * 1000000
    """
    lecturesSum = data.getAllLecturesCount() - solution.getAssignedLecturesSum(data)
    if lecturesSum > 0:
        return lecturesSum * 1000000
    else:
        return 0

def countCurriculumConflicts(solution, slots, data):
    """
    Count the penalty for all lectures which take place at the same time as any other from its curriculum

    :param solution: timetable object
    :param slots: given slots to check
    :param data: whole specification of constraints and regulations
    :return: number of violations * 1000000
    """
    penalty = 0
    for slot in slots:
        curriculums = list()
        for lecture in solution.getTimeTable()[slot]:
            for curriculum in data.getCurriculumForCourseId(lecture[0]):
                if not curriculum in curriculums:
                    curriculums.append(curriculum)
                else:
                    penalty += 1000000

    return penalty


def countRoomOccupancy(solution, slots):
    """
    Counts the penalty for all the lectures which take place in the same room in the same time as any other other lecture

    :param solution: timetable object
    :param slots:
    :return: number of violations * 1000000
    """
    penalty = 0
    for slot in slots:
        rooms = dict()
        for lecture in solution.getTimeTable()[slot]:
            if not lecture[1] in rooms.keys():
                rooms[lecture[1]] = 1
            else:
                penalty += 1000000

    return penalty

def countConstraintsList(solution, slots, data):
    """
    Count penalty for all lectures that are scheduled at the moment when its lecturer is unavailable

    :param solution: timetable object
    :param slots:
    :param data: whole specification of constraints and regulations
    :return: number of violations * 1000000
    """
    penalty = 0
    for slot in slots:
        for lecture in solution.getTimeTable()[slot]:
            for constraint in data.getConstraintsForCourse(lecture[0]):
                if slot == solution.mapKeys(constraint):
                    penalty += 1000000

    return penalty

def countTeachersConflicts(solution, slots, data):
    """
    Count penalty for all teachers who are scheduled to run more than 1 course at the same time

    :param solution: timetable object
    :param slots:
    :param data: whole specification of constraints and regulations
    :return: number of violations * 1000000
    """
    penalty = 0
    for slot in slots:
        teachers = dict()
        for lecture in solution.getTimeTable()[slot]:
            if not data.getCourse(lecture[0]).teacher in teachers.keys():
                teachers[data.getCourse(lecture[0]).teacher] = 1
            else:
                penalty += 1000000

    return penalty

def countRoomTypeViolations(solution, slots, data):
    """
    Count penalty for all lectures scheduled to take place in a room of an inappropriate type

    :param solution: timetable object
    :param slots:
    :param data: whole specification of constraints and regulations
    :return: number of violations * 1000000
    """
    penalty = 0
    for period in slots:
        for lecture in solution.getTimeTable()[period]:
            if data.getCourse(lecture[0]).typeOfRoom != None and data.getCourse(lecture[0]).typeOfRoom != data.getRoom(lecture[1]).type:
                penalty += 1000000

    return penalty