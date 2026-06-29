
from django.urls import path
from .views import ExpenseListCreateView, ExpenseRetrieveUpdateDestroyAPIView
urlpatterns = [
   path('', ExpenseListCreateView.as_view()),
   path('<int:pk>/', ExpenseRetrieveUpdateDestroyAPIView.as_view()),
]
