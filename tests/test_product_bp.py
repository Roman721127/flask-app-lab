import unittest
from app import app

class ProductBlueprintTest(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_products_page(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Продукти".encode("utf-8"), response.data)


if __name__ == "__main__":
    unittest.main()
