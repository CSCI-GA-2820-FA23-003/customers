"""
Customer Service with Swagger

Paths:
------
GET / - Displays a UI for Selenium testing
GET /customers - Returns a list all of the Customers
GET /customers/{id} - Returns the Customer with a given id number
POST /customers - creates a new Customer record in the database
PUT /customers/{id} - updates a Customer record in the database
DELETE /customers/{id} - deletes a Customer record in the database
"""

from flask_restx import Resource, fields, reqparse
from service.common import status  # HTTP Status Codes
from service.models import Customer

# Import Flask application
from . import app, api


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """
    Endpoint to check the health of the microservice.

    Returns:
        A JSON response indicating the health status with HTTP_200_OK.
    """
    return {"status": "OK"}, status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Base URL for our service"""
    return app.send_static_file("index.html")


# Define the model so that the docs reflect what can be sent
create_model = api.model(
    "Customer",
    {
        "first_name": fields.String(
            required=True, description="The first name of the Customer"
        ),
        "last_name": fields.String(
            required=True, description="The last name of the Customer"
        ),
        "email": fields.String(required=True, description="The email of the Customer"),
        "address": fields.String(
            required=True, description="The address of the Customer"
        ),
        "salt": fields.String(required=True, description="The salt of the Customer"),
        "password": fields.String(
            required=True, description="The password of the Customer"
        ),
        "active": fields.Boolean(required=True, description="Is the Customer active?"),
    },
)

customer_model = api.inherit(
    "CustomerModel",
    create_model,
    {
        "id": fields.String(
            readOnly=True, description="The unique id assigned internally by service"
        ),
    },
)

# query string arguments
customer_args = reqparse.RequestParser()
customer_args.add_argument(
    "email",
    type=str,
    location="args",
    required=False,
    help="Search a Customer by email",
)


######################################################################
#  PATH: /customers/{id}
######################################################################
@api.route("/customers/<int:customer_id>")
@api.param("customer_id", "The Customer identifier")
class CustomerResource(Resource):
    """
    CustomerResource class

    Allows the manipulation of a single Customer
    GET /customer{id} - Returns a Customer with the id
    PUT /customer{id} - Update a Customer with the id
    DELETE /customer{id} -  Deletes a Customer with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE A CUSTOMER
    # ------------------------------------------------------------------
    @api.doc("get_customers")
    @api.response(404, "Customer not found")
    @api.marshal_with(customer_model)
    def get(self, customer_id):
        """
        Retrieve a single Customer

        This endpoint will return a Customer based on its id
        """
        app.logger.info("Request to Retrieve a customer with id [%s]", customer_id)
        customer = Customer.find(customer_id)
        if not customer:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Customer with id '{customer_id}' was not found.",
            )

        return customer.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING CUSTOMER
    # ------------------------------------------------------------------
    @api.doc("update_customers")
    @api.response(404, "Customer not found")
    @api.response(400, "The posted Customer data was not valid")
    @api.expect(customer_model)
    @api.marshal_with(customer_model)
    def put(self, customer_id):
        """
        Update a Customer

        This endpoint will update a Customer based on the body that is posted
        """
        app.logger.info("Request to Update a customer with id [%s]", customer_id)
        customer = Customer.find(customer_id)
        if not customer:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Customer with id '{customer_id}' was not found.",
            )
        app.logger.debug("Payload = %s", api.payload)
        data = api.payload
        customer.deserialize(data)
        customer.id = customer_id
        customer.update()
        return customer.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A CUSTOMER
    # ------------------------------------------------------------------
    @api.doc("delete_customers")
    @api.response(204, "Customer deleted")
    def delete(self, customer_id):
        """
        Delete a Customer

        This endpoint will delete a Customer based on the id specified in the path
        """
        app.logger.info("Request to Delete a customer with id [%s]", customer_id)
        customer = Customer.find(customer_id)
        if customer:
            customer.delete()
            app.logger.info("Customer with id [%s] was deleted", customer_id)

        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /customers
######################################################################
@api.route("/customers", strict_slashes=False)
class CustomerCollection(Resource):
    """Handles all interactions with collections of Customers"""

    # ------------------------------------------------------------------
    # LIST ALL CUSTOMERS
    # ------------------------------------------------------------------
    @api.doc("list_customers")
    @api.expect(customer_args, validate=True)
    @api.marshal_list_with(customer_model)
    def get(self):
        """Returns all of the Customers"""
        app.logger.info("Request to list Customers...")
        customers = []
        args = customer_args.parse_args()
        if args["email"]:
            app.logger.info("Filtering by email: %s", args["email"])
            customers = Customer.find_by_email(args["email"])
        else:
            app.logger.info("Returning unfiltered list.")
            customers = Customer.all()

        results = [customer.serialize() for customer in customers]
        app.logger.info("[%s] Customers returned", len(results))
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW CUSTOMER
    # ------------------------------------------------------------------
    @api.doc("create_customers")
    @api.response(400, "The posted data was not valid")
    @api.expect(create_model)
    @api.marshal_with(customer_model, code=201)
    def post(self):
        """
        Creates a Customer
        This endpoint will create a Customer based on the data in the body that is posted
        """
        app.logger.info("Request to Create a Customer")
        customer = Customer()
        app.logger.debug("Payload = %s", api.payload)
        customer.deserialize(api.payload)
        customer.create()
        app.logger.info("Customer with new id [%s] created!", customer.id)
        location_url = api.url_for(
            CustomerResource, customer_id=customer.id, _external=True
        )
        return customer.serialize(), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
#  PATH: /customers/{id}/deactivate
######################################################################
@api.route("/customers/<customer_id>/deactivate")
@api.param("customer_id", "The Customer identifier")
class DeactivateResource(Resource):
    """Deactivate actions on a Customer"""

    @api.doc("deactivate_customers")
    @api.response(404, "Customer not found")
    def put(self, customer_id):
        """
        Deactivate a Customer

        This endpoint will deactivate a Customer
        """
        app.logger.info("Request to Deactivate a Customer")
        customer = Customer.find(customer_id)
        if not customer:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Customer with id [{customer_id}] was not found.",
            )
        customer.active = False
        customer.update()
        app.logger.info("Customer with id [%s] has been deactivated!", customer.id)
        return customer.serialize(), status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def abort(error_code: int, message: str):
    """Logs errors before aborting"""
    app.logger.error(message)
    api.abort(error_code, message)
