__author__ = 'filip'

def countHardConstraints(solution, data):
    """Return sum of penalties"""

    penalty = countRoomCapacityPenalty(solution, solution.getTimeTable().keys(), data)
    penalty += countCurriculumConflicts(solution, solution.getTimeTable().keys(), data)
    penalty += countMissingLectures(solution, data)
    penalty += countRoomOccupancy(solution)
    penalty += countConstraintsList(solution, solution.getTimeTable().keys(), data)
    penalty += countTeachersConflicts(solution, solution.getTimeTable().keys(), data)
    print "Hard Penalty: ", penalty

    return penalty

def checkHardConstraintsForSlots(solution, data, slots):
    penalty = 0
    penalty += countRoomCapacityPenalty(solution, slots, data)
    penalty += countCurriculumConflicts(solution, slots, data)
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
    #print "Kara missing lectures * 2000:", lecturesSum
    if lecturesSum > 0:
        return lecturesSum * 2000
    else:
        return 0

def countCurriculumConflicts(solution, slots, data):
    penalty = 0
    for slot in slots:
        curriculums = dict()
        for lecture in solution.getTimeTable()[slot]:
            for curriculum in data.getCurriculumForCourseId(lecture[0]):
                if not curriculum in curriculums.keys():
                    curriculums[curriculum] = 1
                else:
                    curriculums[curriculum] += 1
        curriculumSum = sum(curriculums.values())
        if curriculumSum > len(curriculums.keys()):
            penalty += (curriculumSum - len(curriculums.keys())) * 100

    return penalty


def countRoomOccupancy(solution):
    penalty = 0
    for slot in solution.getTimeTable().keys():
        rooms = dict()
        for lecture in solution.getTimeTable()[slot]:
            if not lecture[1] in rooms.keys():
                rooms[lecture[1]] = 1
            else:
                penalty += 200

    return penalty

def countConstraintsList(solution, slots, data):
    penalty = 0
    for slot in slots:
        for lecture in solution.getTimeTable()[slot]:
            for constraint in data.getConstraintsForCourse(lecture[0]):
                if slot == solution.mapKeys(constraint):
                    penalty += 200

        return penalty

def countTeachersConflicts(solution, slots, data):
    penalty = 0
    for slot in slots:
        teachers = dict()
        for lecture in solution.getTimeTable()[slot]:
            if not data.getCourse(lecture[0]).teacher in teachers.keys():
                teachers[data.getCourse(lecture[0]).teacher] = 1
            else:
                penalty += 200

    return penalty