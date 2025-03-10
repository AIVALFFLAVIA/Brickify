from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Company

class CompanyModelTest(TestCase):

    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        
        # Create a test company
        self.company = Company.objects.create(
            owner=self.user,
            name="Test Company",
            address="123 Test St, Test City",
            contact_email="test@company.com",
            contact_phone="123-456-7890"
        )

    def test_company_creation(self):
        # Ensure the company was created correctly
        self.assertEqual(self.company.name, "Test Company")
        self.assertEqual(self.company.owner.username, "testuser")
        self.assertEqual(self.company.contact_email, "test@company.com")
        self.assertEqual(self.company.contact_phone, "123-456-7890")
        self.assertEqual(self.company.address, "123 Test St, Test City")

    def test_company_str_method(self):
        # Ensure that the string representation is correct
        self.assertEqual(str(self.company), "Test Company")

    def test_unique_contact_email(self):
        # Try to create another company with the same email
        with self.assertRaises(Exception):  # Expecting a database integrity error
            Company.objects.create(
                owner=self.user,
                name="Another Company",
                address="456 Another St, Another City",
                contact_email="test@company.com",  # Same email should raise an error
                contact_phone="987-654-3210"
            )
