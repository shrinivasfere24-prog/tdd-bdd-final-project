"""REST API routes for the Product Catalog service."""

from flask import jsonify, request
from werkzeug import exceptions
from werkzeug.http import HTTP_STATUS_CODES

from service import app
from service.models import Category, Product, DataValidationError


def check_content_type(content_type):
    """Check that the request contains the expected content type."""
    if not request.is_json:
        raise exceptions.UnsupportedMediaType(
            description=f"Content-Type must be {content_type}"
        )


@app.route("/products", methods=["POST"])
def create_product():
    """Create a new product."""
    check_content_type("application/json")

    product = Product()
    product.deserialize(request.get_json())
    product.create()

    return jsonify(product.serialize()), 201


@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    """Read a product."""
    product = Product.find(product_id)

    if not product:
        raise exceptions.NotFound(
            description=f"Product with id '{product_id}' was not found."
        )

    return jsonify(product.serialize()), 200


@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    """Update a product."""
    check_content_type("application/json")

    product = Product.find(product_id)

    if not product:
        raise exceptions.NotFound(
            description=f"Product with id '{product_id}' was not found."
        )

    product.deserialize(request.get_json())
    product.id = product_id
    product.update()

    return jsonify(product.serialize()), 200


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    """Delete a product."""
    product = Product.find(product_id)

    if product:
        product.delete()

    return "", 204


@app.route("/products", methods=["GET"])
def list_products():
    """List all products or filter by name/category/availability."""
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    if name:
        products = Product.find_by_name(name)

    elif category:
        category_value = getattr(Category, category.upper())
        products = Product.find_by_category(category_value)

    elif available:
        available_value = available.lower() in ["true", "yes", "1"]
        products = Product.find_by_availability(available_value)

    else:
        products = Product.all()

    return jsonify([product.serialize() for product in products]), 200


@app.errorhandler(DataValidationError)
def handle_data_validation_error(error):
    """Handle product validation errors."""
    return jsonify(
        status=HTTP_STATUS_CODES.get(400, "Bad Request"),
        error="Bad Request",
        message=str(error),
    ), 400
