# - In this file, you have to add your tests on Account module.
# - See, app/account.py
# - Test account creation and deletion
# - Use mocks

# Import necessary libraries and modules for testing
import pytest
from unittest.mock import MagicMock

from app.account import Account
from app.database import Database


# Test the account creation process
def test_account_creation(mocker):
    """
    Test the account creation process to ensure it calls the database's add_account method with the correct parameters.
    """
    # Mock the Database class and its add_account method
    mock_db = mocker.MagicMock(spec=Database)
    mock_db.add_account.return_value = (
        1  # Assuming the account creation returns an account ID of 1
    )

    # Create an instance of Account, which should trigger account creation
    account = Account(
        database=mock_db, customer_id=123, account_type="checking", balance=100.0
    )

    # Verify that the Database.add_account method was called once with the correct arguments
    mock_db.add_account.assert_called_once_with(123, "checking", 100.0)

    # Additionally, verify that the account_id is set correctly based on the mocked add_account method's return value
    assert (
        account.account_id == 1
    ), "Account ID should be set to the return value from the database's add_account method."


# Test the account deletion process
def test_account_deletion(mocker):
    """
    Test the account deletion process to ensure it calls the database's delete_account method with the correct account ID.
    """
    # Mock the Database class and its delete_account method
    mock_db = mocker.MagicMock(spec=Database)

    # Create an instance of Account, but don't trigger account creation in the database for this test
    account = Account(database=mock_db)
    # Manually set the account_id for deletion test
    account.account_id = 1

    # Perform account deletion
    account.delete_account(account_id=account.account_id)

    # Verify that the Database.delete_account method was called once with the correct account ID
    mock_db.delete_account.assert_called_once_with(1)


# Note: These tests assume that the Account class's initialization process includes the creation of an account in the database when a customer_id is provided.
# This design may lead to unwanted side effects if not handled properly in real-world applications, such as creating accounts unintentionally during object instantiation.
