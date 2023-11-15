"""
Models for Customer

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


# Function to initialize the database
def init_db(app):
    """Initializes the SQLAlchemy app"""
    Customer.init_db(app)


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class Customer(db.Model):
    """
    Class that represents a Customer
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)

    def __repr__(self):
        return f"<Customer {self.get_full_name()} id=[{self.id}]>"

    def get_full_name(self):
        """
        Returns the Customer's full name
        """
        return f"{self.first_name} {self.last_name}"

    def create(self):
        """
        Creates a Customer to the database
        """
        logger.info("Creating %s", self.get_full_name())
        self.id = None  # pylint: disable=invalid-name
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Customer to the database
        """
        logger.info("Saving %s", self.get_full_name())
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """Removes a Customer from the data store"""
        logger.info("Deleting %s", self.get_full_name())
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes a Customer into a dictionary"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "address": self.address,
            "password": self.password,
            "active": self.active,
        }

    def deserialize(self, data):
        """
        Deserializes a Customer from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.first_name = data["first_name"]
            self.last_name = data["last_name"]
            self.email = data["email"]
            self.address = data["address"]
            self.password = data["password"]
            self.active = data["active"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid Customer: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Customer: body of request contained bad or no data - "
                + "Error message: "
                + str(error)
            ) from error
        return self

    @classmethod
    def init_db(cls, app):
        """Initializes the database session"""
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """Returns all of the Customers in the database"""
        logger.info("Processing all Customers")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a Customer by it's ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_full_name(cls, full_name):
        """Returns all Customers with the given name

        Args:
            name (string): the name of the Customers you want to match
        """
        logger.info("Processing name query for %s ...", full_name)
        name_parts = full_name.split(" ", 1)
        return cls.query.filter(
            cls.first_name == name_parts[0], cls.last_name == name_parts[1]
        )
