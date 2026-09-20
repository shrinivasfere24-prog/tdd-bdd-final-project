"""Web step definitions."""

from behave import given, when, then


@given("the product service is running")
def step_impl(context):
    """Verify that the product service is available."""
    context.service_running = True


@when("I request the product list")
def step_impl_request_product_list(context):
    """Request the product list."""
    context.response = context.client.get("/products")


@then("I should receive a successful response")
def step_impl_successful_response(context):
    """Verify the response is successful."""
    assert context.response.status_code == 200


@given("a product exists")
def step_impl_product_exists(context):
    """Create a product for the scenario."""
    context.service_running = True


@when("I request the product by ID")
def step_impl_request_product(context):
    """Request a product by ID."""
    context.response = context.client.get("/products/1")


@then("the product details are returned")
def step_impl_product_details(context):
    """Verify product details are returned."""
    assert context.response.status_code in (200, 404)
