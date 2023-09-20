from django.shortcuts import redirect, render
from .forms import ExpenseForm, Expense
from django.db.models import Sum
import datetime


def index(request):
    if request.method == "POST":
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.save()

    expenses = Expense.objects.all()
    total = expenses.aggregate(Sum('amount'))

    # last_year total
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    last_year_expense = Expense.objects.filter(date__gt=last_year)
    yearly_sum = last_year_expense.aggregate(Sum('amount'))

    # last_year total
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    last_month_expense = Expense.objects.filter(date__gt=last_month)
    monthly_sum = last_year_expense.aggregate(Sum('amount'))

    # last_year total
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    last_week_expense = Expense.objects.filter(date__gt=last_week)
    weekly_sum = last_year_expense.aggregate(Sum('amount'))
    
    expense_form = ExpenseForm()
    return render(request, 'expense/index.html', {'expense_form':expense_form, 'expenses':expenses, 'total':total})


def edit(request, id):
    expense = Expense.objects.get(id=id)
    expense_form = ExpenseForm(instance=expense)
    if request.method == "POST":
        expense = Expense.objects.get(id=id)
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')
        
    return render(request, 'expense/edit.html', {'expense_form':expense_form})


def delete(request, id):
    if request.method == "POST" and 'delete' in request.POST:
        expense = Expense.objects.get(id=id)
        expense.delete()
    return redirect('index')
