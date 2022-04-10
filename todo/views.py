from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Prefetch, F
from django.http import HttpResponse
from django.shortcuts import render, redirect, resolve_url, get_object_or_404 
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, CreateView, ListView, DeleteView

from .forms import UserForm, ListForm, CardForm, CardCreateFromHomeForm
from . models import List, Card
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

class ListCreateView(LoginRequiredMixin, CreateView):
    model = List
    template_name = "todo/lists/create.html"
    form_class = ListForm
    success_url = reverse_lazy("todo:lists_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ListListView(LoginRequiredMixin, ListView):
    model = List
    template_name = "todo/lists/list.html"

class ListDetailView(LoginRequiredMixin, DetailView):
    model = List
    template_name = "todo/lists/detail.html"

class ListUpdateView(LoginRequiredMixin, UpdateView):
    model = List
    template_name = "todo/lists/update.html"
    form_class = ListForm
    success_url = reverse_lazy("todo:home")

class ListDeleteView(LoginRequiredMixin, DeleteView):
    model = List
    template_name = "todo/lists/delete.html"
    success_url = reverse_lazy("todo:home")

class CardCreateView(LoginRequiredMixin, CreateView):
    model = Card
    template_name = "todo/cards/create.html"
    form_class = CardForm
    success_url = reverse_lazy("todo:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CardListView(LoginRequiredMixin, ListView):
    model = Card
    template_name = "todo/cards/list.html"

class CardDetailView(LoginRequiredMixin, DetailView):
    model = Card
    template_name = "todo/cards/detail.html"

class CardUpdateView(LoginRequiredMixin, UpdateView):
    model = Card
    template_name = "todo/cards/update.html"
    form_class = CardForm
    success_url = reverse_lazy("todo:home")

class CardDeleteView(LoginRequiredMixin, DeleteView):
    model = Card
    template_name = "todo/cards/delete.html"
    success_url = reverse_lazy("todo:home")

class HomeView(LoginRequiredMixin, ListView):
    queryset = List.objects.prefetch_related(Prefetch('card_set', queryset=Card.objects.order_by('order')))
    template_name = "todo/home.html"

class CardCreateFromHomeView(LoginRequiredMixin, CreateView):
    model = Card
    template_name = "todo/cards/create.html" 
    form_class = CardCreateFromHomeForm
    success_url = reverse_lazy("todo:home")

    def form_valid(self, form):
        list_pk = self.kwargs['list_pk']
        list_instance = get_object_or_404(List, pk=list_pk)
        form.instance.list = list_instance
        form.instance.user = self.request.user
        return super().form_valid(form)


def api_card_drag(request):
    card = get_object_or_404(Card, pk=request.POST['cardPk'])
    list_ = get_object_or_404(List, pk=request.POST['listPk'])

    # ドラッグアンドドロップしたカードが抜けた後の、下側にあったデータの並びを-1する
    Card.objects.filter(list=card.list, order__gt=card.order).update(order=F('order')-1)

    insert_target_pk = request.POST.get('insertTarget')
    if insert_target_pk is None:
        # 挿入先リストにまだカードがない場合か、カードとカードの間ではなくカードの親エリアの部分でドロップした
        try:
            # カードの間ではなくカードの親エリアの部分なら、そのlist内で一番大きい値(つまり最後に置く)
            card.order = Card.objects.filter(list=list_).latest('order').order + 1
        except Card.DoesNotExist:
            # 挿入先にデータがない場合、1にする
            card.order = 1

    else:
        # 挿入先にデータがある場合

        # 挿入先の基準のカード
        insert_target_card = get_object_or_404(Card, pk=insert_target_pk)

        if request.POST['insertKind'] == 'before':
            # そのカードの手前に挿入された
            insert_order = insert_target_card.order
        else:
            # そのカードの後に挿入された
            insert_order = insert_target_card.order + 1
        
        # ドラッグアンドドロップしたカードが入った後の、下側にあるデータの並びを+1する
        Card.objects.filter(list=insert_target_card.list, order__gte=insert_order).exclude(pk=card.pk).update(order=F('order')+1)

        card.order = insert_order

    card.list = list_
    card.save()
    return HttpResponse('ok')
