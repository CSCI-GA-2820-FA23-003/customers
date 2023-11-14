"""
My Service

Describe what your service does here
"""

from flask import jsonify, request, url_for, abort, json
from service.common import status  # HTTP Status Codes
from service.models import Customer, DataValidationError

# Import Flask application
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Customer REST API Service",
            version="1.0",
            paths=url_for("list_customers", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################
@app.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    """
    Delete a Customer

    This endpoint will delete a Customer based the id specified in the path
    """
    app.logger.info("Request to delete customer with id: %s", customer_id)
    customer = Customer.find(customer_id)
    if customer:
        customer.delete()
    app.logger.info("Customer with ID [%s] delete complete.", customer_id)
    return "", status.HTTP_204_NO_CONTENT


@app.route("/customers", methods=["POST"])
def create_customer():
    """
    Creates a Customer
    This endpoint will create a Customer based the data in the body that is posted
    """

    # Ensure the request contains JSON data
    app.logger.info("Request to create a customer")
    check_content_type("application/json")

    # Get the JSON data from the request
    data = request.get_json()

    # # Ensure all required fields are in the data
    # required_fields = ["first_name", "last_name", "email", "address"]
    # for field in required_fields:
    #     if field not in data:
    #         return jsonify({"error": f"'{field}' is a required field"}), status.HTTP_400_BAD_REQUEST

    # Create a new Customer with the data
    try:
        customer = Customer()
        customer.deserialize(data)
        customer.create()
    except DataValidationError as error:
        return jsonify({"error": str(error)}), status.HTTP_400_BAD_REQUEST

    location_url = url_for("get_customer", customer_id=customer.id, _external=True)
    app.logger.info("Customer with ID [%s] created.", customer.id)

    # Return the new Customer as JSON
    return (
        jsonify(customer.serialize()),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    """
    Get a Customer

    This endpoint will get a Customer information based the id specified in the path
    """
    customer = Customer.find(customer_id)
    if not customer:
        abort(status.HTTP_404_NOT_FOUND, f"Customer Id: '{customer_id}' was not found.")

    app.logger.info("Customer with ID [%s] get.", customer_id)
    return jsonify(customer.serialize()), status.HTTP_200_OK


@app.route("/customers", methods=["GET"])
def list_customers():
    """
    List all Customers

    This endpoint will retrieve and return a list of all customers
    """
    app.logger.info("Request to list all customers")
    customers = Customer.all()
    return jsonify([customer.serialize() for customer in customers]), status.HTTP_200_OK


@app.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    """
    Update a Customer

    This endpoint will update a Customer based on the data in the body that is put
    """
    app.logger.info("Request to update customer with id: %s", customer_id)

    check_content_type("application/json")

    existing_customer = Customer.find(customer_id)
    if not existing_customer:
        abort(status.HTTP_404_NOT_FOUND, f"Customer Id: '{customer_id}' was not found.")

    updated_data = request.get_json()

    app.logger.info(
        "Updating customer with ID [%s]. New data: %s",
        customer_id,
        json.dumps(updated_data, indent=2),
    )

    existing_customer.deserialize(updated_data)
    existing_customer.update()

    app.logger.info("Customer with ID [%s] updated.", customer_id)
    return jsonify(existing_customer.serialize()), status.HTTP_200_OK

@app.route('/health')
def health():
    return jsonify({"status": "OK"}), 200

######################################################################
# DEACTIVATE A CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>/deactivate", methods=["PUT"])
def deactivate_customer(customer_id):
    """Deactivate a Customer"""
    customer = Customer.find(customer_id)
    if not customer:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Customer with id '{customer_id}' was not found.",
        )

    customer.active = False
    customer.update()

    return customer.serialize(), status.HTTP_200_OK


@app.route("/", methods=["POST", "PUT", "DELETE"])
@app.route("/customers", methods=["PUT", "DELETE"])
def handle_method_not_supported():
    """Handle invalid HTTP method used on an endpoint"""
    abort(status.HTTP_405_METHOD_NOT_ALLOWED)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )
