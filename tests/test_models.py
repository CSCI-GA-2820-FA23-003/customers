"""
Test cases for Customer Model

"""
import os
import logging
import unittest
from service.models import Customer, DataValidationError, db
from service import app


######################################################################
#  Customer   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestCustomer(unittest.TestCase):
    """ Test Cases for Customer Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Pet.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """

    def setUp(self):
        """ This runs before each test """

    def tearDown(self):
        """ This runs after each test """

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_example_replace_this(self):
        """ It should always be true """
        self.assertTrue(True)
