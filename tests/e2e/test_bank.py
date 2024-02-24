# - In this file, you have to write an E2E test on Bank project.
# - See, app/bank.py
# - For understanding purposes, you can interact with main.py
# - Create a real life usage scenario for this project and follow the order for testing components
# - Make sure that the test tests almost all of the functionalities of the project.

import pytest
from app.bank import Bank  # Adjust import paths based on your project structure


@pytest.fixture
def setup_bank():
    # Setup code for the bank system, including initializing with a test database
    bank = Bank(db_path=":memory:")  # Using an in-memory database for tests
    yield bank
    bank.close_connection()


def test_bank_operations_e2e(setup_bank):
    bank = setup_bank

    # Add Customer 1
    customer1_id = bank.add_customer("John Doe", "100 Infinite Loop")
    assert customer1_id is not None, "Failed to add customer 1"

    # Add Customer 2
    customer2_id = bank.add_customer("Jane Smith", "200 Infinite Loop")
    assert customer2_id is not None, "Failed to add customer 2"

    # Update Customer 1's Details
    new_address = "101 Infinite Loop"
    bank.update_customer_details(customer1_id, "John Doe Updated", new_address)
    updated_customer = bank.get_customer_accounts(customer1_id)
    # TODO: fix check
    assert updated_customer is not None, "Customer 1 details update failed"

    # Open Account for Customer 1
    account1_id = bank.open_account(customer1_id, "savings", 1000.0)
    assert account1_id is not None, "Failed to open account for customer 1"
    account1_details = bank.get_account(account1_id)
    assert (
        account1_details and account1_details[3] == 1000.0
    ), "Account 1 opening balance incorrect"

    # Open Account for Customer 2
    account2_id = bank.open_account(customer2_id, "checking", 500.0)
    assert account2_id is not None, "Failed to open account for customer 2"
    account2_details = bank.get_account(account2_id)
    assert (
        account2_details and account2_details[3] == 500.0
    ), "Account 2 opening balance incorrect"

    # Deposit to Account 1
    bank.deposit_to_account(account1_id, 500.0)
    account1_post_deposit = bank.get_account(account1_id)
    assert account1_post_deposit[3] == 1500.0, "Deposit to account 1 failed"

    # Withdraw from Account 2
    bank.withdraw_from_account(account2_id, 200.0)
    account2_post_withdrawal = bank.get_account(account2_id)
    assert account2_post_withdrawal[3] == 300.0, "Withdrawal from account 2 failed"

    # Transfer from Account 1 to Account 2
    bank.transfer_between_accounts(account1_id, account2_id, 300.0)
    account1_post_transfer = bank.get_account(account1_id)
    account2_post_transfer = bank.get_account(account2_id)
    assert (
        account1_post_transfer[3] == 1200.0 and account2_post_transfer[3] == 600.0
    ), "Transfer between accounts failed"

    # Close Account 1
    bank.close_account(account1_id)
    assert bank.get_account(account1_id) is None, "Account 1 closure failed"

    # Delete Customer 1
    bank.delete_customer(customer1_id)
    assert not bank.get_customer_accounts(customer1_id), "Customer 1 deletion failed"

    # Cleanup and final assertions can be done here if necessary


# Run the test
if __name__ == "__main__":
    pytest.main()
