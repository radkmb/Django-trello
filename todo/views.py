from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, resolve_url
from django.views.generic import DetailView, UpdateView

from .forms import UserForm
from .mixins import OnlyYouMixin

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

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "todo/users/detail.html"

class UserUpdateView(OnlyYouMixin, UpdateView):
    model = User
    template_name = "todo/users/update.html"
    form_class = UserForm

    def get_success_url(self):
        return resolve_url('todo:users_detail', pk=self.kwargs['pk'])
