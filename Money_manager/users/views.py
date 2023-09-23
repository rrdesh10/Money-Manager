from django.shortcuts import render, redirect
from .forms import RegisterForm

# Create your views here.
def register_view(request):
    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('login')
    else:
        user_form = RegisterForm()
        return render(request, 'users/register.html', {'user_form':user_form})
    
