from app import app
from currency_code_validation import valid_codes
from unittest import TestCase

class ForexTests(TestCase):
    
    def setUp(self):
        """Things to do before each test is run."""
        self.client = app.test_client()
        app.config["TESTING"] = True

    def test_display_inputs(self):
        """On load, make sure that the form and input fields are properly displayed."""

        with self.client as client:
                resp = client.get('/')
                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 200)

                self.assertIn("Converting from", html)
                self.assertIn("Converting to", html)
                self.assertIn("Amount", html)
                self.assertIn('<button class="btn btn-outline-secondary">Convert</button>', html)
                self.assertIn('<button class="btn btn-outline-secondary" id="reset">Reset</button>', html)

    def test_valid_currency_code(self):
        """Test whether currency code is valid"""

        self.assertIn("AED", valid_codes)
        self.assertNotIn("aed", valid_codes)
        self.assertNotIn("A", valid_codes)
        self.assertNotIn("a", valid_codes)
        self.assertNotIn("YYY", valid_codes)
        self.assertNotIn("YYYY", valid_codes)
        self.assertNotIn(123,valid_codes)
        self.assertNotIn("123", valid_codes)
        self.assertNotIn("", valid_codes)


    def test_conv_from_error(self):
        """Test whether error message displays if user enters invalid 'converting from' currency code"""

        with self.client as client:
            resp = client.get("/convert?convert-from=yyy&convert-to=gbp&amount=100")
            html = resp.get_data(as_text=True)

            self.assertIn("Not a valid code:", html)


    def test_conv_to_error(self):
        """Test whether error message displays if user enters invalid 'converting to' currency code"""

        with self.client as client:
            resp = client.get("/convert?convert-from=usd&convert-to=zzz&amount=100")
            html = resp.get_data(as_text=True)

            self.assertIn("Not a valid code:", html)
         

    def test_amount_error(self):
        """Test whether error message displays if user enters invalid amount"""
        
        with self.client as client:
            resp = client.get("/convert?convert-from=usd&convert-to=gbp&amount=-1")
            html = resp.get_data(as_text=True)

            self.assertIn("Not a valid amount", html)

            resp = client.get("/convert?convert-from=usd&convert-to=gbp&amount=hi")
            html = resp.get_data(as_text=True)

            self.assertIn("Not a valid amount", html)

    def test_conversion_result(self):
        """Test whether correct result of conversion is displayed, rounded to two decimal places, including currency code"""
        with self.client as client:
            resp = client.get("/convert?convert-from=usd&convert-to=usd&amount=5.73064")

            html = resp.get_data(as_text=True)

            self.assertIn("The result is", html)
            self.assertIn("5.73 ", html)
            self.assertIn("USD", html)