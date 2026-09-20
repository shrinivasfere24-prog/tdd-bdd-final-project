"""Unit tests for the Product model."""

import unittest

from service import app
from service.models import Product
from tests.factories import ProductFactory


class TestProductModel(unittest.TestCase):
    """Test Product model operations."""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""
        cls.app = app
        cls.app.config["TESTING"] = True

    def setUp(self):
        """Run before every test."""
        self.client = self.app.test_client()

        with self.app.app_context():
            Product.query.delete()
            from service.models import db
            db.session.commit()

    def tearDown(self):
        """Clean database after every test."""
        with self.app.app_context():
            from service.models import db
            db.session.remove()

    def test_read_a_product(self):
        """Test reading a product."""
        with self.app.app_context():
            product = ProductFactory()
            product.id = None
            product.create()

            found_product = Product.find(product.id)

            self.assertIsNotNone(found_product)
            self.assertEqual(found_product.id, product.id)
            self.assertEqual(found_product.name, product.name)
            self.assertEqual(
                found_product.description,
                product.description,
            )

    def test_update_a_product(self):
        """Test updating a product."""
        with self.app.app_context():
            product = ProductFactory()
            product.id = None
            product.create()

            original_id = product.id
            product.description = "testing"
            product.update()

            self.assertEqual(product.id, original_id)
            self.assertEqual(product.description, "testing")

    def test_delete_a_product(self):
        """Test deleting a product."""
        with self.app.app_context():
            product = ProductFactory()
            product.create()

            self.assertEqual(len(Product.all()), 1)

            product.delete()

            self.assertEqual(len(Product.all()), 0)

    def test_list_all_products(self):
        """Test listing all products."""
        with self.app.app_context():
            self.assertEqual(Product.all(), [])

            for _ in range(5):
                ProductFactory().create()

            self.assertEqual(len(Product.all()), 5)

    def test_find_by_name(self):
        """Test searching products by name."""
        with self.app.app_context():
            products = ProductFactory.create_batch(10)

            for product in products:
                product.create()

            name = products[0].name
            found = Product.find_by_name(name)

            self.assertTrue(
                all(product.name == name for product in found)
            )

    def test_find_by_category(self):
        """Test searching products by category."""
        with self.app.app_context():
            products = ProductFactory.create_batch(10)

            for product in products:
                product.create()

            category = products[0].category
            found = Product.find_by_category(category)

            self.assertTrue(
                all(product.category == category for product in found)
            )

    def test_find_by_availability(self):
        """Test searching products by availability."""
        with self.app.app_context():
            products = ProductFactory.create_batch(10)

            for product in products:
                product.create()

            available = products[0].available
            found = Product.find_by_availability(available)

            self.assertTrue(
                all(product.available == available for product in found)
            )


if __name__ == "__main__":
    unittest.main()
