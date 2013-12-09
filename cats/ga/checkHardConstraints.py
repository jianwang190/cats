__author__ = 'filip'

def countHardConstraints(solution, data):
    """Return sum of penalties"""

    penalty = countCurriculumConflicts(solution, solution.getTimeTable().keys(), data)
    penalty += countMissingLectures(solution, data)
    penalty += countRoomOccupancy(solution, solution.getTimeTable().keys())
    penalty += countConstraintsList(solution, solution.getTimeTable().keys(), data)
    penalty += countTeachersConflicts(solution, solution.getTimeTable().keys(), data)

    return penalty

def checkHardConstraintsForSlots(solution, data, slots):
    penalty = countCurriculumConflicts(solution, slots, data)
    penalty += countRoomOccupancy(solution, slots)
    penalty += countConstraintsList(solution, slots, data)
    penalty += countTeachersConflicts(solution, slots, data)

    return penalty

def countRoomCapacityPenalty(solution, slots, data):
    penalty = 0
    for period in slots:
        for lecture in solution.getTimeTable()[period]:
            overDose = data.getCourse(lecture[0]).studentsNum - data.getRoom(lecture[1]).capacity
            if overDose > 0:
                penalty += (overDose * 10)

    return penalty

def countMissingLectures(solution, data):
    lecturesSum = data.getAllLecturesCount() - solution.getAssignedLecturesSum(data)
    if lecturesSum > 0:
        return lecturesSum * 20000
    else:
        return 0

def countCurriculumConflicts(solution, slots, data):
    penalty = 0
    for slot in slots:
        curriculums = list()
        for lecture in solution.getTimeTable()[slot]:
            for curriculum in data.getCurriculumForCourseId(lecture[0]):
                if not curriculum in curriculums:
                    curriculums.append(curriculum)
                else:
                    penalty += 1000

    return penalty


def countRoomOccupancy(solution, slots):
    penalty = 0
    for slot in slots:
        rooms = dict()
        for lecture in solution.getTimeTable()[slot]:
            if not lecture[1] in rooms.keys():
                rooms[lecture[1]] = 1
            else:
                penalty += 2000

    return penalty

def countConstraintsList(solution, slots, data):
    penalty = 0
    for slot in slots:
        for lecture in solution.getTimeTable()[slot]:
            for constraint in data.getConstraintsForCourse(lecture[0]):
                if slot == solution.mapKeys(constraint):
                    penalty += 2000

    return penalty

def countTeachersConflicts(solution, slots, data):
    penalty = 0
    for slot in slots:
        teachers = dict()
        for lecture in solution.getTimeTable()[slot]:
            if not data.getCourse(lecture[0]).teacher in teachers.keys():
                teachers[data.getCourse(lecture[0]).teacher] = 1
            else:
                penalty += 2000

    return penalty