from calendar import month_name

from django.db.models import (
    Sum,
    Avg,
    Max,
    Min,
    Count,
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from expenses.models import ExpenseModel, BudgetModel

from .serializers import AnalyzeSerializer
from .services import analyze_expenses


class AnalyzeAPIView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = AnalyzeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        month = serializer.validated_data["month"]
        year = serializer.validated_data["year"]

        expenses = ExpenseModel.objects.filter(
            user=request.user,
            date__month=month,
            date__year=year,
        )

        if not expenses.exists():
            return Response(
                {
                    "message": "No expenses found for the selected month."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        summary = expenses.aggregate(
            spent=Sum("amount"),
            total_transactions=Count("id"),
            highest_expense=Max("amount"),
            lowest_expense=Min("amount"),
            average_expense=Avg("amount"),
        )

        budget = BudgetModel.objects.filter(
            user=request.user,
            month=month,
            year=year,
        ).first()

        budget_amount = budget.budget if budget else 0

        spent = summary["spent"] or 0

        remaining = budget_amount - spent

        percentage_used = 0

        if budget_amount > 0:
            percentage_used = round(
                (spent / budget_amount) * 100,
                2,
            )

        category_summary = (
            expenses
            .values("category")
            .annotate(total=Sum("amount"))
            .order_by("-total")
        )

        recurring_expenses = expenses.filter(
            is_recurring=True
        )

        expense_data = f"""
Month: {month_name[month]} {year}

Budget: ₹{budget_amount}

Total Spent: ₹{spent}

Remaining Budget: ₹{remaining}

Budget Used: {percentage_used}%

Total Transactions: {summary['total_transactions']}

Highest Expense: ₹{summary['highest_expense'] or 0}

Lowest Expense: ₹{summary['lowest_expense'] or 0}

Average Expense: ₹{summary['average_expense'] or 0}

Category Breakdown:
"""

        for category in category_summary:

            expense_data += (
                f"\n- {category['category']}: ₹{category['total']}"
            )

        expense_data += "\n\nRecurring Expenses:\n"

        if recurring_expenses.exists():

            for expense in recurring_expenses:

                expense_data += (
                    f"\n- {expense.item} - ₹{expense.amount}"
                )

        else:

            expense_data += "\nNone"

        expense_data += "\n\nRecent Expenses:\n"

        recent_expenses = expenses.order_by("-date", "-id")[:10]

        for expense in recent_expenses:

            expense_data += (
                f"\n- {expense.date} | "
                f"{expense.item} | "
                f"{expense.category} | "
                f"₹{expense.amount}"
            )

        try:

            analysis = analyze_expenses(
                expense_data
            )

            return Response(
                {
                    "month": month_name[month],
                    "year": year,
                    "budget": budget_amount,
                    "spent": spent,
                    "remaining": remaining,
                    "percentage_used": percentage_used,
                    "analysis": analysis,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            return Response(
                {
                    "error": "Failed to generate AI insights.",
                    "details": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )