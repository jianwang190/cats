import unittest


class ReadTest(unittest.TestCase):
    def test_read(self):
        print "HURRA!"
        self.assertTrue(1==1, "dziala!")

    def test_2(self):
        self.assertTrue(2==1)

if __name__=="__main__":
    unittest.main()
