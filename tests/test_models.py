"""
Test cases for Customer Model

"""
# import os
import logging
import unittest

from service.models import Customer, DataValidationError, db
from service import app, config
from tests.factories import CustomerFactory


######################################################################
#  Customer   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestCustomer(unittest.TestCase):
    """Test Cases for Customer Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Customer.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Customer).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_customer(self):
        """It should Create a customer and assert that it exists"""
        customer = Customer(
            first_name="Jorge",
            last_name="Wagner",
            email="jwagner@example.com",
            address="778 Brown Plaza\nNorth Jenniferfurt, VT 88077",
            password="Pa55W0rd",
            active=True,
        )
        self.assertTrue(customer is not None)
        self.assertEqual(customer.id, None)
        self.assertEqual(str(customer), "<Customer Jorge Wagner id=[None]>")
        self.assertEqual(customer.first_name, "Jorge")
        self.assertEqual(customer.last_name, "Wagner")
        self.assertEqual(customer.email, "jwagner@example.com")
        self.assertEqual(
            customer.address, "778 Brown Plaza\nNorth Jenniferfurt, VT 88077"
        )
        self.assertEqual(customer.password, "Pa55W0rd")
        self.assertEqual(customer.active, True)

    def test_add_a_customer(self):
        """It should Create a customer and add it to the database"""
        customers = Customer.all()
        self.assertEqual(customers, [])
        customer = Customer(
            first_name="Jorge",
            last_name="Wagner",
            email="jwagner@example.com",
            address="778 Brown Plaza\nNorth Jenniferfurt, VT 88077",
            password="Pa55W0rd",
            active=True,
        )
        self.assertTrue(customer is not None)
        self.assertEqual(customer.id, None)
        customer.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(customer.id)
        customers = Customer.all()
        self.assertEqual(len(customers), 1)

    def test_read_a_customer(self):
        """It should Read a Customer"""
        customer = CustomerFactory()
        logging.debug(customer)
        customer.id = None
        customer.create()
        self.assertIsNotNone(customer.id)
        # Fetch it back
        found_customer = Customer.find(customer.id)
        self.assertEqual(found_customer.id, customer.id)
        self.assertEqual(found_customer.first_name, customer.first_name)
        self.assertEqual(found_customer.last_name, customer.last_name)
        self.assertEqual(found_customer.email, customer.email)
        self.assertEqual(found_customer.address, customer.address)
        self.assertEqual(found_customer.password, customer.password)
        self.assertEqual(found_customer.active, customer.active)

    def test_update_a_customer(self):
        """It should Update a Customer"""
        customer = CustomerFactory()
        logging.debug(customer)
        customer.id = None
        customer.create()
        logging.debug(customer)
        self.assertIsNotNone(customer.id)
        # Change it an save it
        customer.last_name = "Snow"
        original_id = customer.id
        customer.update()
        self.assertEqual(customer.id, original_id)
        self.assertEqual(customer.last_name, "Snow")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        customers = Customer.all()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].id, original_id)
        self.assertEqual(customers[0].last_name, "Snow")

    def test_update_no_id(self):
        """It should not Update a Customer with no id"""
        customer = CustomerFactory()
        logging.debug(customer)
        customer.id = None
        self.assertRaises(DataValidationError, customer.update)

    def test_delete_a_customer(self):
        """It should Delete a Customer"""
        customer = CustomerFactory()
        customer.create()
        self.assertEqual(len(Customer.all()), 1)
        # delete the customer and make sure it isn't in the database
        customer.delete()
        self.assertEqual(len(Customer.all()), 0)

    def test_list_all_customers(self):
        """It should List all Customers in the database"""
        customers = Customer.all()
        self.assertEqual(customers, [])
        # Create 5 Customers
        for _ in range(5):
            customer = CustomerFactory()
            customer.create()
        # See if we get back 5 customers
        customers = Customer.all()
        self.assertEqual(len(customers), 5)

    def test_serialize_a_customer(self):
        """It should serialize a Customer"""
        customer = CustomerFactory()
        data = customer.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], customer.id)
        self.assertIn("first_name", data)
        self.assertEqual(data["first_name"], customer.first_name)
        self.assertIn("last_name", data)
        self.assertEqual(data["last_name"], customer.last_name)
        self.assertIn("email", data)
        self.assertEqual(data["email"], customer.email)
        self.assertIn("address", data)
        self.assertEqual(data["address"], customer.address)
        self.assertIn("password", data)
        self.assertEqual(data["password"], customer.password)
        self.assertIn("active", data)
        self.assertEqual(data["active"], customer.active)

    def test_deserialize_a_customer(self):
        """It should de-serialize a Customer"""
        data = CustomerFactory().serialize()
        customer = Customer()
        customer.deserialize(data)
        self.assertNotEqual(customer, None)
        self.assertEqual(customer.id, None)
        self.assertEqual(data["first_name"], customer.first_name)
        self.assertEqual(data["last_name"], customer.last_name)
        self.assertEqual(data["email"], customer.email)
        self.assertEqual(data["address"], customer.address)
        self.assertEqual(data["password"], customer.password)
        self.assertEqual(data["active"], customer.active)

    def test_deserialize_missing_data(self):
        """It should not deserialize a Customer with missing data"""
        data = {
            "id": 1,
            "first_name": "Vanessa",
            "email": "vanessa3@yahoo.com",
            "address": "3513 John Divide Suite 115\nRodriguezside, LA 93111",
            "active": "True",
        }
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "this is not a dictionary"
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)

    def test_find_customer(self):
        """It should Find a Customer by ID"""
        customers = CustomerFactory.create_batch(5)
        for customer in customers:
            customer.create()
        logging.debug(customers)
        # make sure they got saved
        self.assertEqual(len(Customer.all()), 5)
        # find the 2nd customer in the list
        customer = Customer.find(customers[1].id)
        self.assertIsNot(customer, None)
        self.assertEqual(customer.id, customers[1].id)
        self.assertEqual(customer.first_name, customers[1].first_name)
        self.assertEqual(customer.last_name, customers[1].last_name)
        self.assertEqual(customer.email, customers[1].email)
        self.assertEqual(customer.address, customers[1].address)
        self.assertEqual(customer.active, customers[1].active)

    def test_find_by_name(self):
        """It should Find a Customer by Name"""
        customers = CustomerFactory.create_batch(10)
        for customer in customers:
            customer.create()
        full_name = customers[0].get_full_name()
        count = len(
            [
                customer
                for customer in customers
                if customer.get_full_name() == full_name
            ]
        )
        found = Customer.find_by_full_name(full_name)
        self.assertEqual(found.count(), count)
        for customer in found:
            self.assertEqual(customer.get_full_name(), full_name)

    def test_find_by_email(self):
        """It should Find a Customer by Email"""
        customers = CustomerFactory.create_batch(10)
        for customer in customers:
            customer.create()
        email = customers[0].email
        count = len([customer for customer in customers if customer.email == email])
        found = Customer.find_by_email(email)
        self.assertEqual(found.count(), count)
        for customer in found:
            self.assertEqual(customer.email, email)
