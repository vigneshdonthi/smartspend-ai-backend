
from django.urls import path
from .views import DashboardAPIView, ExpenseListCreateAPIView, ExpenseRetrieveUpdateDestroyAPIView, BudgetListCreateAPIView, BudgetRetrieveUpdateDestroyAPIView,MonthlySummaryAPIView,CategorySummaryAPIView
urlpatterns = [
   path('', ExpenseListCreateAPIView.as_view()),
   path('<int:pk>/', ExpenseRetrieveUpdateDestroyAPIView.as_view()),
   path("budgets/", BudgetListCreateAPIView.as_view(), name="budget-list-create"),
   path("budgets/<int:pk>/", BudgetRetrieveUpdateDestroyAPIView.as_view(), name="budget-retrieve-update-destroy"),
   path('dashboard/', DashboardAPIView.as_view(), name='dashboard'),
   path('monthly-summary/', MonthlySummaryAPIView.as_view(), name='monthly-summary'),
   path('category-summary/', CategorySummaryAPIView.as_view(), name='category-summary'),
]

