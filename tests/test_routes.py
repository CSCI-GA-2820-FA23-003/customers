"""
Customer API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import json

# import os
import logging
from unittest import TestCase

from service import app, config
from service.common import status  # HTTP Status Codes
from service.models import Customer, db, init_db
from tests.factories import CustomerFactory

# from flask import url_for
# from flask import jsonify


BASE_URL = "/customers"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestCustomerServer(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""

        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""

        db.session.close()

    def setUp(self):
        """This runs before each test"""
        self.client = app.test_client()
        db.session.query(Customer).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    def _create_customers(self, count):
        """Factory method to create customers in bulk"""
        customers = []
        for _ in range(count):
            test_customer = CustomerFactory()
            response = self.client.post(BASE_URL, json=test_customer.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test customer",
            )
            new_customer = response.get_json()
            test_customer.id = new_customer["id"]
            customers.append(test_customer)
        return customers

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], "Customer REST API Service")

    def test_delete_customer(self):
        """It should Delete a Customer"""
        test_customer = self._create_customers(1)[0]
        response = self.client.delete(f"{BASE_URL}/{test_customer.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
        # make sure they are deleted
        response = self.client.get(f"{BASE_URL}/{test_customer.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_customer(self):
        """Create a new Customer"""
        # Arrange
        fake_customer = CustomerFactory()
        data = json.dumps(
            {
                "id": fake_customer.id,
                "first_name": fake_customer.first_name,
                "last_name": fake_customer.last_name,
                "email": fake_customer.email,
                "address": fake_customer.address,
                "password": fake_customer.password,
                "active": fake_customer.active,
            }
        )

        # Action
        response = self.client.post(
            "/customers", data=data, content_type="application/json"
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the data is correct
        new_json = json.loads(response.data)
        self.assertEqual(new_json["first_name"], fake_customer.first_name)
        self.assertEqual(new_json["last_name"], fake_customer.last_name)
        self.assertEqual(new_json["email"], fake_customer.email)
        self.assertEqual(new_json["address"], fake_customer.address)
        self.assertEqual(new_json["password"], fake_customer.password)
        self.assertEqual(new_json["active"], fake_customer.active)

    def test_create_customer_wrong_field(self):
        """Create a new Customer with wrong field"""
        # Arrange
        fake_customer = CustomerFactory()
        data = json.dumps(
            {
                "id": fake_customer.id,
                "firstName": fake_customer.first_name,
                "lastName": fake_customer.last_name,
                "email": fake_customer.email,
                "address": fake_customer.address,
                "password": fake_customer.password,
                "active": fake_customer.active,
            }
        )

        # Action
        response = self.client.post(
            "/customers", data=data, content_type="application/json"
        )

        # Check the data is correct
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_customer_no_json(self):
        """Create a new Customer with no JSON data"""

        # Convert the data to a string instead of JSON
        data = json.dumps({})

        # Action
        response = self.client.post(
            "/customers", data=data, content_type="application/json"
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_customer_not_json(self):
        """Create a new Customer with non-JSON data"""
        # Arrange
        fake_customer = CustomerFactory()

        # Convert the data to a string instead of JSON
        data = str(
            {
                "id": fake_customer.id,
                "first_name": fake_customer.first_name,
                "last_name": fake_customer.last_name,
                "email": fake_customer.email,
                "address": fake_customer.address,
                "password": fake_customer.password,
                "active": fake_customer.active,
            }
        )

        # Action
        response = self.client.post(
            "/customers",
            data=data,
            content_type="text/plain",  # Send as plain text instead of JSON
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_customer_no_type(self):
        """Create a new Customer with no content_type"""
        # Arrange
        fake_customer = CustomerFactory()

        # Convert the data to a string instead of JSON
        data = str(
            {
                "id": fake_customer.id,
                "first_name": fake_customer.first_name,
                "last_name": fake_customer.last_name,
                "email": fake_customer.email,
                "address": fake_customer.address,
                "password": fake_customer.password,
                "active": fake_customer.active,
            }
        )

        # Action
        response = self.client.post(
            "/customers",
            data=data,
            # Send as no type instead of JSON
        )

        # Assert
        self.assertEqual(
            response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        )  # Expect a 400 error

    def test_create_customer_missing_field(self):
        """Create a new Customer with missing fields"""
        # Arrange
        fake_customer = CustomerFactory()
        data_dict = {
            "id": fake_customer.id,
            "first_name": fake_customer.first_name,
            "last_name": fake_customer.last_name,
            "email": fake_customer.email,
            "address": fake_customer.address,
            "password": fake_customer.password,
            "active": fake_customer.active,
        }

        required_fields = ["first_name", "last_name", "email", "address", "active"]

        for key in required_fields:
            bad_data = data_dict.copy()

            # Remove a required field
            del bad_data[key]

            # Action
            response = self.client.post(
                "/customers", data=json.dumps(bad_data), content_type="application/json"
            )

            # Assert
            self.assertEqual(
                response.status_code, status.HTTP_400_BAD_REQUEST
            )  # Expect a 400 error

            # Check the error message
            error_json = json.loads(response.data)
            self.assertEqual(error_json["error"], "Invalid Customer: missing " + key)

    def test_get_customer(self):
        """It should Read a Customer"""
        # customer = CustomerFactory()
        # logging.debug(customer)
        # customer.id = None
        # customer.create()
        # self.assertIsNotNone(customer.id)
        # # Fetch it back
        # found_customer = Customer.find(customer.id)
        # self.assertEqual(found_customer.id, customer.id)
        # self.assertEqual(found_customer.first_name, customer.first_name)
        # self.assertEqual(found_customer.last_name, customer.last_name)
        # self.assertEqual(found_customer.email, customer.email)
        # self.assertEqual(found_customer.address, customer.address)

        # Create a test resource using the factory
        customer = CustomerFactory()

        response = self.client.get(
            "/customers/" + str(customer.id),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        customer.create()

        # Send a GET request to retrieve the resource
        response = self.client.get(
            "/customers/" + str(customer.id),
        )

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        customer = Customer.find(customer.id)
        found_customer = response.get_json()

        # Check if the returned JSON data matches the resource data
        self.assertEqual(found_customer, customer.serialize())

    def test_list_customers(self):
        """Test listing all customers"""
        # Get the current number of customers before creating new ones
        initial_customer_count = len(self.client.get(BASE_URL).get_json())

        self._create_customers(3)
        response = self.client.get(BASE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        customers_data = response.get_json()
        self.assertIsInstance(customers_data, list)

        expected_length = initial_customer_count + 3

        self.assertEqual(len(customers_data), expected_length)

    def test_update_existing_customer(self):
        """Test updating an existing customer should return 200_OK"""
        original_customer = self._create_customers(1)[0]
        updated_customer = CustomerFactory()

        response = self.client.put(
            f"{BASE_URL}/{original_customer.id}", json=updated_customer.serialize()
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_customer_data = response.get_json()
        self.assertEqual(
            updated_customer_data["first_name"], updated_customer.first_name
        )
        self.assertEqual(updated_customer_data["last_name"], updated_customer.last_name)
        self.assertEqual(updated_customer_data["email"], updated_customer.email)
        self.assertEqual(updated_customer_data["address"], updated_customer.address)
        self.assertEqual(updated_customer_data["password"], updated_customer.password)
        self.assertEqual(updated_customer_data["active"], updated_customer.active)

    def test_update_non_existing_customer(self):
        """Test updating a non-existing customer should return 404_NOT_FOUND"""
        non_existing_customer_id = 9999
        updated_customer = CustomerFactory()

        response = self.client.put(
            f"{BASE_URL}/{non_existing_customer_id}", json=updated_customer.serialize()
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        expected_error_message = f"404 Not Found: Customer Id: '{non_existing_customer_id}' was not found."
        self.assertEqual(response.get_json()["message"], expected_error_message)

    def test_deactivate_a_customer(self):
        """It should Deactivate a Customer"""
        customer = self._create_customers(1)[0]
        response = self.client.get(f"{BASE_URL}/{customer.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        logging.debug("Response data: %s", data)
        self.assertEqual(data["active"], True)

        response = self.client.put(f"{BASE_URL}/{customer.id}/deactivate")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        logging.debug("Response data: %s", data)
        self.assertEqual(data["active"], False)

    def test_deactivate_a_nonexistent_customer(self):
        """It should Not Deactivate a Nonexistent Customer"""
        customer = self._create_customers(1)[0]
        response = self.client.put(f"{BASE_URL}/{customer.id + 1}/deactivate")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_method_not_supported(self):
        """It should return a HTTP_405_METHOD_NOT_ALLOWED when an unsupported method is called on an endpoint"""
        response = self.client.post("/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put("/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.delete("/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.delete(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_health(self):
        """Send Request and Test status_code as 200_OK, JSON content as status: OK"""
        response = self.client.get("/health")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json, {"status": "OK"})
