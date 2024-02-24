# - In this file, you have to add your tests on Customer module.
# - See, app/customer.py
# - Test customer creation, loading, updating and deletion
# - Use mocks

import pytest
from unittest.mock import MagicMock
from app.database import Database

# Assuming the Customer class is in a module named customer_management.py
from app.customer import Customer


# Test customer creation
def test_customer_creation(mocker):
    """
    Test the customer creation to ensure it calls the database's add_customer method correctly.
    """
    # Mock the Database class and its add_customer method
    mock_db = mocker.MagicMock(spec=Database)
    mock_db.add_customer.return_value = (
        1  # Assume adding a customer returns a customer ID of 1
    )

    # Create an instance of Customer, triggering the customer creation process
    customer = Customer(database=mock_db, name="John Doe", address="123 Elm Street")

    # Verify the Database.add_customer method was called once with the correct arguments
    mock_db.add_customer.assert_called_once_with("John Doe", "123 Elm Street")

    # Ensure the customer_id is set correctly based on the mocked add_customer method's return value
    assert (
        customer.customer_id == 1
    ), "Customer ID should be set to the return value from the database's add_customer method."


# Test loading a customer
def test_load_customer(mocker):
    """
    Test loading a customer's details to ensure it properly sets the object's attributes.
    """
    mock_db = mocker.MagicMock(spec=Database)
    mock_db.get_customer.return_value = (2, "Jane Doe", "456 Oak Street")

    customer = Customer(database=mock_db, customer_id=2)

    # Validate that the customer details are loaded correctly
    assert (
        customer.name == "Jane Doe" and customer.address == "456 Oak Street"
    ), "Customer details should be loaded into the object attributes."


# Test updating a customer
def test_update_customer_details(mocker):
    """
    Test the update of a customer's details to ensure it calls the database's update_customer method correctly.
    """
    mock_db = mocker.MagicMock(spec=Database)

    customer = Customer(database=mock_db, customer_id=3)
    customer.update_details("New Name", "New Address")

    # Verify the Database.update_customer method was called once with the correct arguments
    mock_db.update_customer.assert_called_once_with(3, "New Name", "New Address")


# Test deleting a customer
def test_delete_customer(mocker):
    """
    Test customer deletion to ensure it calls the database's delete_customer method with the correct customer ID.
    """
    mock_db = mocker.MagicMock(spec=Database)

    customer = Customer(database=mock_db, customer_id=4)
    customer.delete_customer()

    # Verify the Database.delete_customer method was called once with the correct customer ID
    mock_db.delete_customer.assert_called_once_with(4)


# Note: It's crucial to ensure that the mocked methods return values that match what you'd expect from the actual database operations where necessary.
# This setup helps in mimicking the real interactions and ensuring the test conditions are as close to the real application scenario as possible.
