CAPACITY_PENALTY = 1
MIN_WORKINGS_DAY_PENALTY = 5
COMPACTNESS_PENALTY = 2
STABILITY_PENALTY = 1


def countPenaltyForCurriculumCompactnessPerturbation(periodsList, periodsPerDay, perturbation, perturbationPenalty):
    """
    Count curriculum compactness penalty for one curriculum
    :param periodsList: list with slots for curriculum (when the course of curriculum took place)
    :param periodsPerDay: periods per day in timetable
    :return:
    """
    if perturbation == "perturbation":
        penalty = 0
        for i in range(0, len(periodsList)):
            if i > 0 and periodsList[i - 1][2] + 1 == periodsList[i][2] and (periodsList[i - 1][2] / periodsPerDay == periodsList[i][2] / periodsPerDay):
                beforeLecture = True
            else:
                beforeLecture = False
            if i < len(periodsList) - 1 and (periodsList[i + 1][2] - 1 == periodsList[i][2]) and (periodsList[i + 1][2] / periodsPerDay == periodsList[i][2] / periodsPerDay):
                afterLecture = True
            else:
                afterLecture = False
            if beforeLecture is False and afterLecture is False:
                perturbationPenalty[(periodsList[i][0], periodsList[i][1], periodsList[i][2])] += 1 * COMPACTNESS_PENALTY
                penalty += 1
    else:
        penalty = countPenaltyForCurriculumCompactness(periodsList, periodsPerDay)
    return {'penalty': penalty, 'perturbationPenalty': perturbationPenalty}


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


def totalSoftConstraintsForTimetable2(partialTimetable, data):
    result = softConstraintsPenalty(partialTimetable, data)
    return result['penaltyMinWorkingDays'] + result['penaltyCurriculumCompactness']


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
            perturbationPenalty[(cell[0], cell[1], key)] = roomCapacityPenalty * CAPACITY_PENALTY
            information[cell[0]][0].add(cell[1])
            information[cell[0]][1].add(key / data.periodsPerDay)
            if perturbation is not None:
                map(lambda x: curPeriodDict[x.id].append((cell[0], cell[1], key)), data.getCurriculumForCourseId(cell[0]))
            else:
                map(lambda x: curPeriodDict[x.id].append(key), data.getCurriculumForCourseId(cell[0]))


    if perturbation is not None:
        curriculumCompactnessPenalty = 0
        for x in curPeriodDict:
            result = countPenaltyForCurriculumCompactnessPerturbation(curPeriodDict[x], data.periodsPerDay, "perturbation", perturbationPenalty)
            perturbationPenalty = result['perturbationPenalty']
            curriculumCompactnessPenalty += result['penalty']
    else:
        curriculumCompactnessPenalty = sum(map(lambda x: countPenaltyForCurriculumCompactness(\
            curPeriodDict[x], data.periodsPerDay), curPeriodDict))

    for key in information.keys():
        stabilityPenalty = len(information[key][0]) - 1 if len(information[key][0]) > 1 else 0
        workingDaysPenalty = data.getCourse(key).minWorkingDays - len(information[key][1])\
            if data.getCourse(key).minWorkingDays > len(information[key][1]) else 0
        roomStabilityPenalty += stabilityPenalty
        minWorkingDaysPenalty += workingDaysPenalty
        tempPenalty = stabilityPenalty * STABILITY_PENALTY + workingDaysPenalty * MIN_WORKINGS_DAY_PENALTY

        if perturbation is not None:
            for x in perturbationPenalty.keys():
                if x[0] == key:
                    perturbationPenalty[x] += tempPenalty


    roomStabilityPenalty *= STABILITY_PENALTY
    minWorkingDaysPenalty *= MIN_WORKINGS_DAY_PENALTY
    roomCapacityPenalty *= CAPACITY_PENALTY
    curriculumCompactnessPenalty *= COMPACTNESS_PENALTY

    penalty = roomStabilityPenalty + minWorkingDaysPenalty + roomCapacityPenalty + curriculumCompactnessPenalty

    return {'penaltyMinWorkingDays': minWorkingDaysPenalty, 'penaltyRoomStability': roomStabilityPenalty,\
            'penaltyRoomCapacity': roomCapacityPenalty,'penaltyCurriculumCompactness': curriculumCompactnessPenalty,\
            'totalPenalty': penalty, 'perturbationPenalty': perturbationPenalty}

