"""
TestCustomerModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from service import app
from service.models import db
from service.common import status  # HTTP Status Codes

import json
from tests.factories import CustomerFactory
from service.models import Customer
from flask import jsonify

######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestCustomerServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """

    def setUp(self):
        """ This runs before each test """
        self.client = app.test_client()

    def tearDown(self):
        """ This runs after each test """

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
        
    def test_get_customer(self):
        # """It should Read a Customer"""
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
        
        
