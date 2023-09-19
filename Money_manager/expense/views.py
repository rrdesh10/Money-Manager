from django.shortcuts import render
from .forms import ExpenseForm


def index(request):
    expense_form = ExpenseForm()
    return render(request, 'expense/index.html', {'expense_form':expense_form})
