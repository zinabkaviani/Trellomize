import pytest
import bcrypt
from unittest import mock
from register import encode_password,check_password ,check_email_format, is_valid_username, is_username_length_valid,\
                     check_existing_username, check_existing_email, admin_username_check, admin_email_check

def test_encode_password():
    password = "testpassword"
    hashed = encode_password(password)
    assert bcrypt.checkpw(password.encode('utf-8'), hashed)

def test_check_password():
    password = "testpassword"
    hashed = encode_password(password).decode('utf-8')
    assert check_password(password, hashed)
    assert not check_password("wrongpassword", hashed)

@pytest.mark.parametrize("email,expected", [
    ("test@gmail.com", True),
    ("test@yahoo.com", True),
    ("test@outlook.com", True),
    ("test@hotmail.com", True),
    ("test@live.com", True),
    ("test@aol.com", True),
    ("test@example.com", False),
    ("test@.com", False),
    ("test@com", False),
])
def test_check_email_format(email, expected):
    assert check_email_format(email) == expected

@pytest.mark.parametrize("username,expected", [
    ("validUser", True),
    ("invalid@User", False),
    ("anotherInvalidUser#", False),
    ("Valid123", True),
    ("Invalid!@#", False),
])
def test_is_valid_username(username, expected):
    assert is_valid_username(username) == expected

@pytest.mark.parametrize("username,expected", [
    ("short", True),
    ("aVeryLongUsernameIndeed", False),
    ("exactly15Chars", True),
    ("16CharactersHere", False),
])
def test_is_username_length_valid(username, expected):
    assert is_username_length_valid(username) == expected

def test_check_existing_username(tmp_path):
    d = tmp_path / "Data/Accounts_Data"
    d.mkdir(parents=True)
    p = d / "users.txt"
    p.write_text("existingUser,someemail@gmail.com\n")

    with mock.patch("os.path.exists", return_value=True):
        with mock.patch("builtins.open", mock.mock_open(read_data="existingUser,someemail@gmail.com\n")):
            assert check_existing_username("existingUser")
            assert not check_existing_username("newUser")

def test_check_existing_email(tmp_path):
    d = tmp_path / "Data/Accounts_Data"
    d.mkdir(parents=True)
    p = d / "users.txt"
    p.write_text("someUser,existingemail@gmail.com\n")

    with mock.patch("os.path.exists", return_value=True):
        with mock.patch("builtins.open", mock.mock_open(read_data="someUser,existingemail@gmail.com\n")):
            assert check_existing_email("existingemail@gmail.com")
            assert not check_existing_email("newemail@gmail.com")

def test_admin_username_check(tmp_path):
    d = tmp_path / "Manager"
    d.mkdir(parents=True)
    p = d / "manager.txt"
    p.write_text("adminUser,someemail@gmail.com\n")

    with mock.patch("os.path.exists", return_value=True):
        with mock.patch("builtins.open", mock.mock_open(read_data="adminUser,someemail@gmail.com\n")):
            assert admin_username_check("adminUser")
            assert not admin_username_check("nonAdminUser")

def test_admin_email_check(tmp_path):
    d = tmp_path / "Manager"
    d.mkdir(parents=True)
    p = d / "manager.txt"
    p.write_text("someUser,adminemail@gmail.com\n")

    with mock.patch("os.path.exists", return_value=True):
        with mock.patch("builtins.open", mock.mock_open(read_data="someUser,adminemail@gmail.com\n")):
            assert admin_email_check("adminemail@gmail.com")
            assert not admin_email_check("nonadminemail@gmail.com")
