CAPACITY_PENALTY = 1
MIN_WORKINGS_DAY_PENALTY = 5
COMPACTNESS_PENALTY = 2
STABILITY_PENALTY = 1


def countPenaltyForCurriculumCompactness(periodsList, periodsPerDay):
    """
    Count curriculum compactness penalty for one curriculum
    :param periodsList: list with slots for curriculum (when the course of curriculum took place)
    :param periodsPerDay: periods per day in timetable
    :return:
    """
    penalty = 0
    for i in range(0, len(periodsList)):
        if i > 0 and periodsList[i - 1] + 1 == periodsList[i] and (periodsList[i - 1] / periodsPerDay == periodsList[i] / periodsPerDay):
            beforeLecture = True
        else:
            beforeLecture = False
        if i < len(periodsList) - 1 and (periodsList[i + 1] - 1 == periodsList[i]) and (periodsList[i + 1] / periodsPerDay == periodsList[i] / periodsPerDay):
            afterLecture = True
        else:
            afterLecture = False
        if beforeLecture is False and afterLecture is False:
            penalty += 1
    return penalty


def totalSoftConstraintsForTimetable(partialTimetable, data):
    """
    Get total soft constrains penalty for timetable
    :param partialTimetable: timetable for which soft constraints penalty is counted
    :param data: data describing courses
    :return: total soft constraints penalty
    """
    return softConstraintsPenalty(partialTimetable, data)['totalPenalty']


def softConstraintsPenalty(partialTimetable, data, perturbation = None):
    """
    Count soft penalty for timetable
    perturbation penalty for each lecture include : room stability penalty, room capacity, min workings days
    :param partialTimetable: timetable to grade
    :param data: data for tested timetable
    :return: dictionary with penalty for : min working days, curriculum compactness, room stability and capacity, total penalty
    """
    roomCapacityPenalty = 0
    roomStabilityPenalty = 0
    minWorkingDaysPenalty = 0
    # room Set, workingDays
    information = {x.id: [set(), set()] for x in data.getAllCourses()}
    curPeriodDict = {x.id: [] for x in data.getAllCurricula()}

    # dictionary with penalties necessary to perturbation phase
    # courseId : partial penalty (without room capacity
    perturbationPenalty = {}


    for key in partialTimetable.keys():
        for cell in partialTimetable[key]:
            capacityPenalty = data.getCourse(cell[0]).studentsNum - data.getRoom(cell[1]).capacity \
                if data.getCourse(cell[0]).studentsNum > data.getRoom(cell[1]).capacity else 0
            roomCapacityPenalty += capacityPenalty
            perturbationPenalty[(cell, key)] = roomCapacityPenalty * CAPACITY_PENALTY
            information[cell[0]][0].add(cell[1])
            information[cell[0]][1].add(key / data.periodsPerDay)
            map(lambda x: curPeriodDict[x.id].append(key), data.getCurriculumForCourseId(cell[0]))


    curriculumCompactnessPenalty = sum(map(lambda x: countPenaltyForCurriculumCompactness(curPeriodDict[x], data.periodsPerDay), curPeriodDict))

    for key in information.keys():
        stabilityPenalty = len(information[key][0]) - 1 if len(information[key][0]) > 1 else 0
        workingDaysPenalty = data.getCourse(key).minWorkingDays - len(information[key][1])\
            if data.getCourse(key).minWorkingDays > len(information[key][1]) else 0
        roomStabilityPenalty += stabilityPenalty
        minWorkingDaysPenalty += workingDaysPenalty
        tempPenalty = stabilityPenalty * STABILITY_PENALTY + workingDaysPenalty * MIN_WORKINGS_DAY_PENALTY

        if perturbation is not None:
            for cell in perturbationPenalty.keys():
                if cell[0] == key:
                    perturbationPenalty[(cell, key)] += tempPenalty


    roomStabilityPenalty *= STABILITY_PENALTY
    minWorkingDaysPenalty *= MIN_WORKINGS_DAY_PENALTY
    roomCapacityPenalty *= CAPACITY_PENALTY
    curriculumCompactnessPenalty *= COMPACTNESS_PENALTY

    penalty = roomStabilityPenalty + minWorkingDaysPenalty + roomCapacityPenalty + curriculumCompactnessPenalty

    return {'penaltyMinWorkingDays': minWorkingDaysPenalty, 'penaltyRoomStability': roomStabilityPenalty,\
            'penaltyRoomCapacity': roomCapacityPenalty,'penaltyCurriculumCompactness': curriculumCompactnessPenalty,\
            'totalPenalty': penalty, 'perturbationPenalty': perturbationPenalty}

