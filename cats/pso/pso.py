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
        self.h = []

    def run(self):
        self.genParticles()

        for i in range(conf.maxIterations):
            self.doIteration(i)
            self.h.append((i,self.globalBestSolution.penalty))

            if self.globalBestSolution.penalty < conf.minPenalty:
                break

            if time.time() > self.timeLimit:
                break
            #print "------------------------"
            #for p in self.particles:
                #print "Act:", p.actualSolution.penalty
                #print "best:", p.bestSolution.penalty
            print "BEST:", self.globalBestSolution.penalty
                #print "------------------------"
        self.timetableFactory.echo(self.globalBestSolution)
        h2 = []
        for particle in self.particles:
            h2.append(particle.history)

        #print h2
        #print self.h

        return self.globalBestSolution

    def genParticles(self):
        """Generate population of particles"""

        for i in range(conf.populationSize):
            timetable = self.timetableFactory.getRandomTimetable()
            self.particles.append(Particle(timetable, self.timetableFactory))

    def doIteration(self, nr):
        """Do PSO iteration"""

        for particle in self.particles:
            self.evaluate(particle)
            particle.history.append((nr,particle.actualSolution.penalty))
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






