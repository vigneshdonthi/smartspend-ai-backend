from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import ExpenseModel, BudgetModel


class ExpenseBudgetAPITest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="user1",
            password="password123"
        )

        self.user2 = User.objects.create_user(
            username="user2",
            password="password123"
        )

        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        self.expense = ExpenseModel.objects.create(
            user=self.user,
            date="2026-06-29",
            item="Pizza",
            category="Food",
            amount=500,
            notes="Dinner",
            is_recurring=False
        )

        self.other_expense = ExpenseModel.objects.create(
            user=self.user2,
            date="2026-06-29",
            item="Laptop",
            category="Shopping",
            amount=50000,
            notes="Office",
            is_recurring=False
        )

        self.budget = BudgetModel.objects.create(
            user=self.user,
            month=6,
            year=2026,
            budget=5000
        )

    # ---------------- Expense List ----------------

    def test_list_expenses(self):
        response = self.client.get("/api/expenses/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_only_logged_user_expenses(self):
        response = self.client.get("/api/expenses/")
        self.assertEqual(response.data["count"], 1)

    # ---------------- Expense Create ----------------

    def test_create_expense(self):

        data = {
            "date": "2026-06-30",
            "item": "Burger",
            "category": "Food",
            "amount": 250,
            "notes": "Lunch",
            "is_recurring": False
        }

        response = self.client.post("/api/expenses/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_expense(self):

        response = self.client.post("/api/expenses/", {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ---------------- Retrieve ----------------

    def test_get_expense(self):

        response = self.client.get(f"/api/expenses/{self.expense.pk}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_other_user_expense(self):

        response = self.client.get(f"/api/expenses/{self.other_expense.pk}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ---------------- Update ----------------

    def test_update_expense(self):

        response = self.client.put(
            f"/api/expenses/{self.expense.pk}/",
            {
                "amount": 900
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_other_user_expense(self):

        response = self.client.put(
            f"/api/expenses/{self.other_expense.pk}/",
            {
                "amount": 900
            }
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ---------------- Delete ----------------

    def test_delete_expense(self):

        response = self.client.delete(
            f"/api/expenses/{self.expense.pk}/"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_other_user_expense(self):

        response = self.client.delete(
            f"/api/expenses/{self.other_expense.pk}/"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ---------------- Search ----------------

    def test_search_item(self):

        response = self.client.get("/api/expenses/?search=Pizza")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_notes(self):

        response = self.client.get("/api/expenses/?search=Dinner")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ---------------- Filter ----------------

    def test_filter_category(self):

        response = self.client.get("/api/expenses/?category=Food")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_date(self):

        response = self.client.get("/api/expenses/?date=2026-06-29")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_recurring(self):

        response = self.client.get("/api/expenses/?is_recurring=False")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ---------------- Ordering ----------------

    def test_order_amount(self):

        response = self.client.get("/api/expenses/?ordering=amount")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ---------------- Budget ----------------

    def test_budget_list(self):

        response = self.client.get("/api/expenses/budgets/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_budget(self):

        response = self.client.post(
            "/api/expenses/budgets/",
            {
                "month": 7,
                "year": 2026,
                "budget": 7000
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_budget_retrieve(self):

        response = self.client.get(
            f"/api/expenses/budgets/{self.budget.pk}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_budget_delete(self):

        response = self.client.delete(
            f"/api/expenses/budgets/{self.budget.pk}/"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)