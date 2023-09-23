from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    category = models.CharField(max_length=50)
    date = models.DateField(auto_now=True)


    def __str__(self) -> str:
        return self.name