import unittest
from unittest.mock import patch, mock_open
import re
import os

# Assuming the functions are in a module named 'auth'
from register import check_email_format, check_existing_username, check_existing_email

class TestAuthFunctions(unittest.TestCase):
    
    def test_check_email_format(self):
        self.assertTrue(check_email_format("test@gmail.com"))
        self.assertTrue(check_email_format("user@yahoo.com"))
        self.assertFalse(check_email_format("invalid_email.com"))
        self.assertFalse(check_email_format("another@domain.org"))
        self.assertFalse(check_email_format("user@unsupported.net"))

    @patch("builtins.open", new_callable=mock_open, read_data="user1,email1@gmail.com\nuser2,email2@yahoo.com\n")
    @patch("os.path.exists")
    def test_check_existing_username(self, mock_exists, mock_file):
        mock_exists.return_value = True
        self.assertTrue(check_existing_username("user1"))
        self.assertFalse(check_existing_username("user3"))

    @patch("builtins.open", new_callable=mock_open, read_data="user1,email1@gmail.com\nuser2,email2@yahoo.com\n")
    @patch("os.path.exists")
    def test_check_existing_email(self, mock_exists, mock_file):
        mock_exists.return_value = True
        self.assertTrue(check_existing_email("email1@gmail.com"))
        self.assertFalse(check_existing_email("nonexistent@gmail.com"))

if __name__ == '__main__':
    unittest.main()