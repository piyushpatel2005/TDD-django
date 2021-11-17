import unittest
from student import Student

class TestStudent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nsetupClass\n")

    @classmethod
    def tearDownClass(cls):
        print('\nteardownClass')

    def setUp(self):
        self.stu_1 = Student('Robin', 'Wills', 25000)
        self.stu_2 = Student('Mark', 'Smith', 28000)

    def tearDown(self) -> None:
        pass

    def test_mail(self):

        self.assertEqual(self.stu_1.mail, 'Robin.Wills@xyz.com')
        self.assertEqual(self.stu_2.mail, 'Mark.Smith@xyz.com')

        self.stu_1.first = 'Jenifer'
        
        self.assertEqual(self.stu_1.mail, 'Jenifer.Wills@xyz.com')
        self.assertEqual(self.stu_2.mail, 'Mark.Smith@xyz.com')

    def test_fullname(self):

        self.assertEqual(self.stu_1.fullname, 'Robin Wills')
        self.assertEqual(self.stu_2.fullname, 'Mark Smith')

        self.stu_1.first = 'Jenifer'
        
        self.assertEqual(self.stu_1.fullname, 'Jenifer Wills')
        self.assertEqual(self.stu_2.fullname, 'Mark Smith')

    def test_stipend_hike(self):

        self.stu_1.apply_hike()
        self.stu_2.apply_hike()

        self.assertEqual(self.stu_1.stipend, 26250)
        self.assertEqual(self.stu_2.stipend, 29400)

if __name__ == '__main__':
    unittest.main()