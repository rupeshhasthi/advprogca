import unittest
import sys
import os

# Ensure root folder is in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.models import User, Expense


class TestFlaskApp(unittest.TestCase):

    # Setup and Teardown

    def setUp(self):
        """Create a fresh app + database before each test"""
        self.app = create_app(
            test_config={
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
                "WTF_CSRF_ENABLED": False,
                "SECRET_KEY": "test-secret",
            }
        )

        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Destroy database after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def register_user(self, email="test@example.com", password="password"):
        return self.client.post(
            "/register",
            data={
                "email": email,
                "password": password,
                "confirm_password": password,
            },
            follow_redirects=True,
        )

    def login_user(self, email="test@example.com", password="password"):
        return self.client.post(
            "/login",
            data={"email": email, "password": password},
            follow_redirects=True,
        )

    # TEST CASES

    def test1_register(self):
        """Test user registration"""
        response = self.register_user()
        self.assertIn(b"Registration successful", response.data)

    def test2_login(self):
        """Test login works"""
        self.register_user()
        response = self.login_user()
        self.assertIn(b"Logged in successfully", response.data)

    def test3_logout(self):
        """Test logout"""
        self.register_user()
        self.login_user()
        response = self.client.get("/logout", follow_redirects=True)
        self.assertIn(b"Logged out", response.data)

    def test4_dashboard_requires_login(self):
        """Dashboard should redirect if user not logged in"""
        response = self.client.get("/", follow_redirects=True)
        self.assertIn(b"Login", response.data)

    def test5_dashboard_after_login(self):
        """Dashboard should load after login"""
        self.register_user()
        self.login_user()
        response = self.client.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test6_add_expense(self):
        """Test expense creation"""
        self.register_user()
        self.login_user()

        response = self.client.post(
            "/add",
            data={"category": "Food", "amount": 10, "note": "Lunch"},
            follow_redirects=True,
        )

        self.assertIn(b"Expense added", response.data)

        with self.app.app_context():
            self.assertEqual(Expense.query.count(), 1)

    def test7_view_expenses(self):
        """Test expenses page shows added expense"""
        self.register_user()
        self.login_user()

        self.client.post(
            "/add", data={"category": "Travel", "amount": 50, "note": "Taxi"}
        )

        response = self.client.get("/expenses")
        self.assertIn(b"Taxi", response.data)

    def test8_delete_expense(self):
        """Test deleting expense"""
        self.register_user()
        self.login_user()

        self.client.post(
            "/add", data={"category": "Bills", "amount": 100, "note": "Electricity"}
        )

        with self.app.app_context():
            expense = Expense.query.first()
            self.assertIsNotNone(expense)

        response = self.client.post(f"/delete/{expense.id}", follow_redirects=True)
        self.assertIn(b"Expense deleted", response.data)

        with self.app.app_context():
            self.assertEqual(Expense.query.count(), 0)


if __name__ == "__main__":
    unittest.main()
