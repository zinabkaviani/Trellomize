import pytest
from unittest.mock import patch
from Project_Task.project import Project,check_existing_username

# Mocking the globals module
class MockGlobals:
    @staticmethod
    def get_input_with_cancel():
        return "mocked_input"

    # Mock other globals functions used in your Project class as needed
def test_check_existing_username():
    # Write unit tests for check_existing_username function
    with open("Data\\Accounts_Data\\users.txt" ,"w") as file:
        file.write("existing_username,test@gmail.com")

    assert check_existing_username("existing_username") == True
    assert check_existing_username("non_existing_username") == False

