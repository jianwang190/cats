import conf
from particle import Particle
from copy import deepcopy


class PSO(object):
    def __init__(self, data):
        self.data = data
        self.particles = []
        self.globalBest = None
        self.evaluationFunction = EvaluationFunction()

    def run(self):
        self.genParticles()

        for i in range(conf.maxIterations):
            self.doIteration()

        return self.globalBest

    def genParticles(self):
        """Generate population of particles"""

        for i in range(conf.populationSize):
            self.particles.append(Particle())

    def doIteration(self):
        """Do PSO iteration"""

        for particle in self.particles:
            particle.evaluate()
            """
                Napisz funkcje do oceniania
                ktora korzysta z pola penalty
                klasy timetable. Jak penalty == None
                to oblicza u ustawia to pole.
                Najpeliej wrzuc ta funkcje do klasy
                timetable.
            """
            particle.updateLocalBest()
            self.updateGlobalBest(particle)
            particle.produceNewSolution(self.globalBest)

    def updateGlobalBest(self, particle):
        """Update local best solution of particle"""

        if particle.best.penalty < self.globalBest.penalty:
            self.globalBest = deepcopy(particle.best)






