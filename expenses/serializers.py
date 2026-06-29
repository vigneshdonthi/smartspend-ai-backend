from rest_framework import serializers
from .models import BudgetModel, ExpenseModel

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseModel
        fields = "__all__"
        read_only_fields = ['user', 'created_at', 'updated_at']


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetModel
        fields = "__all__"
        read_only_fields = ['user', 'created_at', 'updated_at']