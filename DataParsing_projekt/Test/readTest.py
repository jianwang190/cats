import unittest
from dataParsing.readCSV import DataParser

class ReadTest(unittest.TestCase):
    def setUp(self):
        self.c = DataParser()

    def test_combineIntoGroups(self):
        """
        Test for all translation of data
        :return:
        """
        #self.c.translateData()
        self.c.combineIntoGroups()
        self.c.writeAllCourses()
        self.c.readRooms()
        self.c.writeToOutputFile()
        pass


    def test_readRooms(self):
        """
        Read rooms from file
        @rtype : object
        """
        self.c.translateGroupsOfStudents()
        pass



if __name__=="__main__":
    unittest.main()
