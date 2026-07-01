from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ExpenseModel,BudgetModel

admin.site.register(ExpenseModel)
admin.site.register(BudgetModel)