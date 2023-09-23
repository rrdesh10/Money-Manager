from django.shortcuts import redirect, render
from .forms import ExpenseForm, Expense
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
import datetime


@login_required
def index(request):
    user = request.user

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()

    expenses = Expense.objects.filter(user=user)
    total = expenses.aggregate(Sum('amount'))

    # last_year total
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    last_year_expense = Expense.objects.filter(date__gt=last_year, user=user)
    yearly_sum = last_year_expense.aggregate(Sum('amount'))

    # last_year total
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    last_month_expense = Expense.objects.filter(date__gt=last_month, user=user)
    monthly_sum = last_month_expense.aggregate(Sum('amount'))

    # last_year total
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    last_week_expense = Expense.objects.filter(date__gt=last_week, user=user)
    weekly_sum = last_week_expense.aggregate(Sum('amount'))

    # Daily sum
    daily_sums = Expense.objects.filter(user=user).values('date').order_by('date').annotate(sum=Sum('amount'))

    # Categorical Sum
    category_sums = Expense.objects.filter(user=user).values('category').order_by('category').annotate(sum=Sum('amount'))

    expense_form = ExpenseForm()
    context = {'expense_form':expense_form, 'expenses':expenses, 'total':total, 'yearly_sum':yearly_sum, 
               'monthly_sum':monthly_sum, 'weekly_sum':weekly_sum, 'daily_sums':daily_sums, 'category_sums':category_sums}
    
    return render(request, 'expense/index.html', context)


@login_required
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
