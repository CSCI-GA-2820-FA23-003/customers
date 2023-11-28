"""
Test Factory to make fake objects for testing
"""
import factory
from service.models import Customer
import os
import hashlib


class CustomerFactory(factory.Factory):
    """Creates fake customers"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Customer

    id = factory.Sequence(lambda n: n)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("ascii_email")
    address = factory.Faker("address")
    salt = os.urandom(16).hex()
    password = factory.LazyAttribute(lambda obj: hashlib.sha256(obj.salt.encode() + "P@ssw0rd!123".encode()).hexdigest())
    active = True
