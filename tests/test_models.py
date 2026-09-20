"""Required model-test functions.
Merge these functions into the project's existing TestCase/class and imports.
"""

def test_read_a_product(self):
    product = ProductFactory()
    product.id = None
    product.create()
    self.assertIsNotNone(product.id)
    found_product = Product.find(product.id)
    self.assertEqual(found_product.id, product.id)
    self.assertEqual(found_product.name, product.name)
    self.assertEqual(found_product.description, product.description)
    self.assertEqual(found_product.price, product.price)

def test_update_a_product(self):
    product = ProductFactory()
    product.id = None
    product.create()
    original_id = product.id
    product.description = "testing"
    product.update()
    self.assertEqual(product.id, original_id)
    self.assertEqual(product.description, "testing")

def test_delete_a_product(self):
    product = ProductFactory()
    product.create()
    self.assertEqual(len(Product.all()), 1)
    product.delete()
    self.assertEqual(len(Product.all()), 0)

def test_list_all_products(self):
    self.assertEqual(Product.all(), [])
    for _ in range(5):
        ProductFactory().create()
    self.assertEqual(len(Product.all()), 5)

def test_find_by_name(self):
    products = ProductFactory.create_batch(10)
    for product in products:
        product.create()
    name = products[0].name
    found = Product.find_by_name(name)
    self.assertTrue(all(product.name == name for product in found))

def test_find_by_category(self):
    products = ProductFactory.create_batch(10)
    for product in products:
        product.create()
    category = products[0].category
    found = Product.find_by_category(category)
    self.assertTrue(all(product.category == category for product in found))

def test_find_by_availability(self):
    products = ProductFactory.create_batch(10)
    for product in products:
        product.create()
    available = products[0].available
    found = Product.find_by_availability(available)
    self.assertTrue(all(product.available == available for product in found))
