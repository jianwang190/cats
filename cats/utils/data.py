class Data(object):
    """Store data"""

    def __init__(self):
        self.courses = []
        self.rooms = []
        self.curricula = []
        self.constraints = []
        self.instanceName = ""
        self.daysNum = 0
        self.periodsPerDay = 0
    def __str__(self):
        return " ".join([str(self.daysNum), str(self.periodsPerDay)])




