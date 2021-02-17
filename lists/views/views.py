from django.shortcuts import redirect, render
from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

# Create your views here.
class HomePage(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ItemForm()
        context['count'] = self.request.session.get('count', 1)
        return context


class ShowDetailView(DetailView):
    model = List
    template_name = 'lists/list_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ExistingListItemForm(for_list=self.object)
        return context


def create_item(request, *args, **kwargs):
    list_ = List.objects.get(pk=kwargs['pk'])
    form = ExistingListItemForm(for_list=list_, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(list_)
    return render(request, 'lists/list_detail.html', {
        'list': list_, 'form': form
    })


def new_list(request):
    form = ItemForm(request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})
