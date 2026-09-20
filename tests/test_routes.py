"""Required REST route tests.
Merge these into the project's existing route-test class and imports.
"""

def test_get_product(self):
    test_product = self._create_products(1)[0]
    response = self.client.get(f"{BASE_URL}/{test_product.id}")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    data = response.get_json()
    self.assertEqual(data["name"], test_product.name)

def test_update_product(self):
    test_product = ProductFactory()
    response = self.client.post(BASE_URL, json=test_product.serialize())
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    new_product = response.get_json()
    new_product["description"] = "unknown"
    response = self.client.put(
        f"{BASE_URL}/{new_product['id']}", json=new_product
    )
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.get_json()["description"], "unknown")

def test_delete_product(self):
    products = self._create_products(5)
    test_product = products[0]
    response = self.client.delete(f"{BASE_URL}/{test_product.id}")
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(len(response.data), 0)

def test_get_product_list(self):
    self._create_products(5)
    response = self.client.get(BASE_URL)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.get_json()), 5)

def test_query_by_name(self):
    products = self._create_products(5)
    test_name = products[0].name
    response = self.client.get(
        BASE_URL, query_string=f"name={quote_plus(test_name)}"
    )
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    for product in response.get_json():
        self.assertEqual(product["name"], test_name)

def test_query_by_category(self):
    products = self._create_products(10)
    category = products[0].category
    response = self.client.get(
        BASE_URL, query_string=f"category={category.name}"
    )
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    for product in response.get_json():
        self.assertEqual(product["category"], category.name)

def test_query_by_availability(self):
    self._create_products(10)
    response = self.client.get(
        BASE_URL, query_string="available=true"
    )
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    for product in response.get_json():
        self.assertTrue(product["available"])
