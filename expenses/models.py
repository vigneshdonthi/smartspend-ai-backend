from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ExpenseModel(models.Model):
    CATEGORY_CHOICES = [
        ("Food", "Food"),
        ("Transport", "Transport"),
        ("Entertainment", "Entertainment"),
        ("Shopping", "Shopping"),
        ("Bills", "Bills"),
        ("Groceries", "Groceries"),
        ("HealthCare", "HealthCare"),
        ("Other", "Other"),
    ]
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    date = models.DateField()
    item = models.CharField(max_length=100)
    category = models.CharField(choices = CATEGORY_CHOICES,max_length=100)
    amount= models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Amount(₹)")
    notes = models.TextField(blank=True)
    is_recurring = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item} - ₹{self.amount} - {self.category}"


class BudgetModel(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="budgets"
    )

    month = models.PositiveSmallIntegerField()

    year = models.PositiveSmallIntegerField()

    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Budget (₹)"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["user", "month", "year"],
                name="unique_budget_per_month"
            )
        ]

        ordering = ["-year", "-month"]

    def __str__(self):
        return f"{self.user.username} - {self.month}/{self.year} - ₹{self.budget}"