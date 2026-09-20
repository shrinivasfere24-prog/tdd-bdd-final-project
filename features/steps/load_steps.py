from behave import given
import requests

@given("the following products")
def step_impl(context):
    rest_endpoint = f"{context.base_url}/products"

    response = requests.get(rest_endpoint)
    assert response.status_code == 200

    for product in response.json():
        response = requests.delete(f"{rest_endpoint}/{product['id']}")
        assert response.status_code == 204

    for row in context.table:
        payload = {
            "name": row["name"],
            "description": row["description"],
            "price": row["price"],
            "available": row["available"] in ["True", "true", "1"],
            "category": row["category"],
        }
        response = requests.post(rest_endpoint, json=payload)
        assert response.status_code == 201
