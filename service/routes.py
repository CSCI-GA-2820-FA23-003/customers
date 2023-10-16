"""
My Service

Describe what your service does here
"""

from flask import jsonify, request, url_for, abort
from service.common import status  # HTTP Status Codes
from service.models import Customer, DataValidationError

# Import Flask application
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

# Place your REST API code here ...

@app.route("/customers/<int:customer_id>", methods=['DELETE'])
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
    return jsonify(customer.serialize()), status.HTTP_201_CREATED, {"Location": location_url}

@app.route("/customers/<int:customer_id>", methods=['GET'])
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
