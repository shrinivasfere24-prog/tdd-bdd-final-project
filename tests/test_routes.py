"""REST API tests."""

import unittest
from urllib.parse import quote_plus


from service import app
from service.models import Product, db
from tests.factories import ProductFactory


class TestProductRoutes(unittest.TestCase):
    """Test Product REST API routes."""

    BASE_URL = "/products"

    @classmethod
    def setUpClass(cls):
        """Set up the Flask application."""
        cls.app = app
        cls.app.config["TESTING"] = True

    def setUp(self):
        """Run before every test."""
        self.client = self.app.test_client()

        with self.app.app_context():
            Product.query.delete()
            db.session.commit()

    def _create_products(self, count):
        """Create products for testing."""
        products = ProductFactory.create_batch(count)

        with self.app.app_context():
            for product in products:
                product.id = None
                product.create()

        return products

    def test_get_product(self):
        """Test GET /products/<id>."""
        products = self._create_products(1)
        test_product = products[0]

        response = self.client.get(
            f"{self.BASE_URL}/{test_product.id}"
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["name"], test_product.name)

    def test_update_product(self):
        """Test PUT /products/<id>."""
        test_product = ProductFactory()

        response = self.client.post(
            self.BASE_URL,
            json=test_product.serialize(),
        )

        self.assertEqual(response.status_code, 201)

        new_product = response.get_json()
        new_product["description"] = "unknown"

        response = self.client.put(
            f"{self.BASE_URL}/{new_product['id']}",
            json=new_product,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["description"],
            "unknown",
        )

    def test_delete_product(self):
        """Test DELETE /products/<id>."""
        products = self._create_products(5)
        test_product = products[0]

        response = self.client.delete(
            f"{self.BASE_URL}/{test_product.id}"
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(response.data), 0)

    def test_get_product_list(self):
        """Test GET /products."""
        self._create_products(5)

        response = self.client.get(self.BASE_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 5)

    def test_query_by_name(self):
        """Test filtering products by name."""
        products = self._create_products(5)
        test_name = products[0].name

        response = self.client.get(
            self.BASE_URL,
            query_string=f"name={quote_plus(test_name)}",
        )

        self.assertEqual(response.status_code, 200)

        for product in response.get_json():
            self.assertEqual(product["name"], test_name)

    def test_query_by_category(self):
        """Test filtering products by category."""
        products = self._create_products(10)
        category = products[0].category

        response = self.client.get(
            self.BASE_URL,
            query_string=f"category={category.name}",
        )

        self.assertEqual(response.status_code, 200)

        for product in response.get_json():
            self.assertEqual(product["category"], category.name)

    def test_query_by_availability(self):
        """Test filtering products by availability."""
        self._create_products(10)

        response = self.client.get(
            self.BASE_URL,
            query_string="available=true",
        )

        self.assertEqual(response.status_code, 200)

        for product in response.get_json():
            self.assertTrue(product["available"])


if __name__ == "__main__":
    unittest.main()
