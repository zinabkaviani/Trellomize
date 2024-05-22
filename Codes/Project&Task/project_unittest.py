import unittest
from unittest.mock import patch
from project import project

class TestProject(unittest.TestCase):

    def setUp(self):
        self.project = project(1, "Project 1", ["member1", "member2"], "leader", ["task1", "task2"])

    def test_add_member(self):
        with patch('builtins.input', return_value="new_member"):
            self.project.add_member()
        self.assertIn("new_member", self.project._project__members)

    def test_remove_members(self):
        self.project.remove_members()
        self.assertNotIn("member1", self.project._project__members)

    def test_display_tasks(self):
        with patch('builtins.print') as mock_print:
            self.project.display_tasks()
        mock_print.assert_called()

    def test_add_tasks(self):
        with patch('builtins.input', side_effect=["Task 1", "Description 1"]):
            self.project.add_tasks()
        self.assertEqual(len(self.project._project__tasks), 3)

if __name__ == '__main__':
    unittest.main()
