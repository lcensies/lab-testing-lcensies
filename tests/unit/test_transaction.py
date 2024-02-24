# - In this file, you have to add your tests on Transaction module.
# - See, app/transaction.py
# - Test transaction with different types - deposit, withdraw and transfer
# - Use mocks accordingly

import pytest
from unittest.mock import MagicMock

from app.transaction import Transaction


@pytest.fixture
def mock_database(mocker):
    # Create a mock database object
    mock_db = MagicMock()
    # Configure the mock to return a specific account on get_account
    # Mocking a typical account tuple as would be returned by Database.get_account()
    # account_id, customer_id, account_type, balance
    mock_db.get_account.side_effect = (
        lambda account_id: (account_id, 1, "checking", 100)
        if account_id != 999
        else None
    )
    return mock_db


def test_deposit_positive_amount(mock_database):
    transaction = Transaction(mock_database)
    transaction.deposit(1, 50)

    # Verify balance update and transaction addition
    mock_database.update_account_balance.assert_called_once_with(1, 150)
    mock_database.add_transaction.assert_called_once_with(None, 1, 50, "deposit")


def test_withdraw_sufficient_funds(mock_database):
    transaction = Transaction(mock_database)
    transaction.withdraw(1, 50)

    # Verify balance update and transaction addition
    mock_database.update_account_balance.assert_called_once_with(1, 50)
    mock_database.add_transaction.assert_called_once_with(1, None, 50, "withdrawal")


def test_transfer_sufficient_funds(mock_database):
    transaction = Transaction(mock_database)
    # Setting up the mock to return a different balance for the target account
    mock_database.get_account.side_effect = (
        lambda account_id: (account_id, 2, "savings", 200)
        if account_id == 2
        else (1, 1, "checking", 100)
    )
    transaction.transfer(1, 2, 50)

    # Check updates for both accounts and the transaction record
    calls = [((1, 50),), ((2, 250),)]
    mock_database.update_account_balance.assert_has_calls(calls, any_order=True)
    mock_database.add_transaction.assert_called_once_with(1, 2, 50, "transfer")


# Example of a test case for a failed operation due to insufficient funds
def test_withdraw_insufficient_funds(mock_database):
    transaction = Transaction(mock_database)
    with pytest.raises(ValueError, match="Insufficient funds."):
        transaction.withdraw(1, 150)


# Example of a test case for attempting to operate on a non-existent account
def test_deposit_nonexistent_account(mock_database):
    transaction = Transaction(mock_database)
    with pytest.raises(ValueError, match="Account does not exist."):
        transaction.deposit(999, 100)
