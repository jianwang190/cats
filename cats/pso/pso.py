import time

import conf
from particle import Particle
from copy import deepcopy
from timetable import TimetableFactory
from evaluationFunction import EvaluationFunction


class PSO(object):
    def __init__(self, data, timeLimit):
        self.timeLimit = timeLimit
        self.data = data
        self.particles = []
        self.globalBestSolution = None
        self.timetableFactory = TimetableFactory(data)
        self.evaluationFunction = EvaluationFunction(data, self.timetableFactory)

    def run(self):
        self.genParticles()

        for i in range(conf.maxIterations):
            self.doIteration()

            if self.globalBestSolution.penalty < conf.minPenalty:
                break

            if time.time() > self.timeLimit:
                break
            #print "------------------------"
            #for p in self.particles:
                #print "Act:", p.actualSolution.penalty
                #print "best:", p.bestSolution.penalty
                #print "BEST:", self.globalBestSolution.penalty
                #print "------------------------"

        self.timetableFactory.echo(self.globalBestSolution)
        return self.globalBestSolution

    def genParticles(self):
        """Generate population of particles"""

        for i in range(conf.populationSize):
            timetable = self.timetableFactory.getRandomTimetable()
            self.particles.append(Particle(timetable, self.timetableFactory))

    def doIteration(self):
        """Do PSO iteration"""

        for particle in self.particles:
            self.evaluate(particle)
            particle.updateLocalBestSolution()
            self.updateGlobalBestSolution(particle)
            particle.produceNewSolution(self.globalBestSolution)

    def evaluate(self, particle):
        """Evaluate particle"""

        particle.actualSolution.penalty = self.evaluationFunction.evaluate(particle.actualSolution)

    def updateGlobalBestSolution(self, particle):
        """Update global best solution"""

        if self.globalBestSolution == None:
            self.globalBestSolution = deepcopy(particle.bestSolution)

        if particle.bestSolution.penalty < self.globalBestSolution.penalty:
            self.globalBestSolution = deepcopy(particle.bestSolution)






