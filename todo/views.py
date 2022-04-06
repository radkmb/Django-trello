from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def index(request):
    return render(request, "todo/index.html")

@login_required
def home(request):
    return render(request, "todo/home.html")

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user_instance = form.save()
            login(request, user_instance)
            return redirect("todo:home")
    else:
        form = UserCreationForm()

    context = {
        "form": form
    }
    return render(request, 'todo/signup.html', context)
