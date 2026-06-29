from datetime import date, datetime
from django.db.models.functions import ExtractMonth, ExtractYear
import django
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BudgetModel, ExpenseModel
from .serializers import BudgetSerializer, ExpenseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from rest_framework.filters import SearchFilter,OrderingFilter
#from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import  ExpenseBudgetPagination
from django.db.models import Sum, Avg, Max, Min, Count
'''
class ExpenseListCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        queryset = ExpenseModel.objects.filter(user = request.user)
        serializer = ExpenseSerializer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        # queryset = ExpenseModel.objects.filter(user=self.request.user)

        # search = self.request.query_params.get("search")
        # if search:
        #     queryset = queryset.filter(
        #         Q(item__icontains=search) |
        #         Q(notes__icontains=search)
        #     )

        # category = self.request.query_params.get("category")
        # if category:
        #     queryset = queryset.filter(category=category)

        # date = self.request.query_params.get("date")
        # if date:
        #     queryset = queryset.filter(date=date)

        # start_date = self.request.query_params.get("start_date")
        # if start_date:
        #     queryset = queryset.filter(date__gte=start_date)

        # end_date = self.request.query_params.get("end_date")
        # if end_date:
        #     queryset = queryset.filter(date__lte=end_date)

        # min_amount = self.request.query_params.get("min_amount")
        # if min_amount:
        #     queryset = queryset.filter(amount__gte=min_amount)

        # max_amount = self.request.query_params.get("max_amount")
        # if max_amount:
        #     queryset = queryset.filter(amount__lte=max_amount)

        # recurring = self.request.query_params.get("is_recurring")
        # if recurring:
        #     if recurring.lower() == "true":
        #         queryset = queryset.filter(is_recurring=True)
        #     elif recurring.lower() == "false":
        #         queryset = queryset.filter(is_recurring=False)

        # ordering = self.request.query_params.get("ordering")
        # if ordering:
        #     queryset = queryset.order_by(ordering)

        # return queryset
    def post(self,request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

'''


class ExpenseListCreateAPIView(generics.ListCreateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer
    pagination_class = ExpenseBudgetPagination

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "category",
        "is_recurring",
        "date",
    ]

    search_fields = [
        "item",
        "notes",
    ]

    ordering_fields = [
        "date",
        "amount",
        "category",
        "item",
    ]

    ordering = ["-date"]

    def get_queryset(self):
        return ExpenseModel.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




class ExpenseRetrieveUpdateDestroyAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        try:
            expense = ExpenseModel.objects.get(pk=pk,user=request.user)
            serializer = ExpenseSerializer(expense)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except ExpenseModel.DoesNotExist:
            return Response({"error":"Expense not found"},status=status.HTTP_404_NOT_FOUND)
    def put(self,request,pk):
        try:
            expense = ExpenseModel.objects.get(pk=pk,user=request.user)
        except ExpenseModel.DoesNotExist:
            return Response({"error":"Expense not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = ExpenseSerializer(expense,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        try:
            expense = ExpenseModel.objects.get(pk=pk,user=request.user)
        except ExpenseModel.DoesNotExist:
            return Response({"error":"Expense not found"},status=status.HTTP_404_NOT_FOUND)
        expense.delete()
        return Response({"message": "Expense deleted successfully"},status=status.HTTP_204_NO_CONTENT)


class BudgetListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetSerializer
    pagination_class = ExpenseBudgetPagination
    def get_queryset(self):
        return BudgetModel.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BudgetRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return BudgetModel.objects.filter(user=self.request.user)





class DashboardAPIView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        today = date.today()

        month = request.query_params.get("month", today.month)
        year = request.query_params.get("year", today.year)
        if month < 1 or month > 12:
            return Response(
                {"error": "Invalid month"},
                    status=400
                )
        expenses = ExpenseModel.objects.filter(
            user=request.user,
            date__month=month,
            date__year=year,
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
            percentage_used = round((spent / budget_amount) * 100, 2)

        recent_expenses = expenses.order_by("-date", "-id")[:5]

        serializer = ExpenseSerializer(
            recent_expenses,
            many=True
        )

        return Response(
            {
                "month": int(month),
                "year": int(year),
                "budget": budget_amount,
                "spent": spent,
                "remaining": remaining,
                "percentage_used": percentage_used,
                "total_transactions": summary["total_transactions"],
                "highest_expense": summary["highest_expense"],
                "lowest_expense": summary["lowest_expense"],
                "average_expense": summary["average_expense"],
                "recent_expenses": serializer.data,
            }
        )


class MonthlySummaryAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):

        monthly_summary = (
            ExpenseModel.objects.filter(user=request.user)
            .annotate(
                month=ExtractMonth("date"),
                year=ExtractYear("date")
            )
            .values("month", "year")
            .annotate(total=Sum("amount"))
            .order_by("year", "month")
        )

        return Response(
            monthly_summary,
            status=status.HTTP_200_OK
        )
class CategorySummaryAPIView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        today = date.today()

        category_summary = (
            ExpenseModel.objects.filter(
                user=request.user,
                date__month=today.month,
                date__year=today.year,
            )
            .values("category")
            .annotate(total=Sum("amount"))
            .order_by("category")
        )

        return Response(category_summary,status=200)

