import conf
from particle import Particle
from copy import deepcopy


class PSO(object):
    def __init__(self, data, evaluationFunction):
        self.data = data
        self.particles = []
        self.globalBestSolution = None
        self.evaluationFunction = evaluationFunction
        self.timeTableFactory = TimetableFactory(data)

    def run(self):
        self.genParticles()

        for i in range(conf.maxIterations):
            self.doIteration()

        return self.globalBestSolution

    def genParticles(self):
        """Generate population of particles"""

        for i in range(conf.populationSize):
            timetable = self.timeTableFactory.getRandomTimetable()
            self.particles.append(Particle(timetable))

    def doIteration(self):
        """Do PSO iteration"""

        for particle in self.particles:
            self.evaluate(particle)
            particle.updateLocalBestSoluton()
            self.updateGlobalBestSoluton(particle)
            particle.produceNewSolution(self.globalBestSolution)

    def evaluate(self, particle):
        """Evaluate particle"""
        particle.actual.penalty = self.evaluationFunction.evaluate(particle.actual)

    def updateGlobalBestSoluton(self, particle):
        """Update global best solution"""

        if self.globalBestSolution == None:
            self.globalBestSolution = particle.best

        if particle.bestSoluton.penalty < self.globalBestSolution.penalty:
            self.globalBestSolution = deepcopy(particle.best)






