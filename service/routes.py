"""Required route functions.
Merge these functions into the project's existing service/routes.py,
keeping its existing imports, app setup, and helper functions.
"""

@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    product = Product.find(product_id)
    if not product:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Product with id '{product_id}' was not found."
        )
    return product.serialize(), status.HTTP_200_OK

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    check_content_type("application/json")
    product = Product.find(product_id)
    if not product:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Product with id '{product_id}' was not found."
        )
    product.deserialize(request.get_json())
    product.id = product_id
    product.update()
    return product.serialize(), status.HTTP_200_OK

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    product = Product.find(product_id)
    if product:
        product.delete()
    return "", status.HTTP_204_NO_CONTENT

@app.route("/products", methods=["GET"])
def list_products():
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

    return [product.serialize() for product in products], status.HTTP_200_OK
