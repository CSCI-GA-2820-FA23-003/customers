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

@app.route("/customers", methods=["POST"])
def create_customer():
    """ Create a Customer """

    # Ensure the request contains JSON data
    if not request.is_json:
        return jsonify({"error": "The request payload is not in JSON format"}), status.HTTP_400_BAD_REQUEST
    
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
    
    # Return the new Customer as JSON
    return jsonify(customer.serialize()), status.HTTP_201_CREATED

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
