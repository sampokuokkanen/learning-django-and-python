from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from lists.models import Item, List
from lists.forms import ItemForm


# Create your views here.
def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        item = Item(text=request.POST.get('text', None), list=list_)
        try:
            item.full_clean()
            item.save()
            return redirect(f'/lists/{list_.id}/')
        except ValidationError:
            error = "You can't have an empty list item"

    return render(request, 'list.html', {'list': list_, "error": error})


def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST.get('text', None), list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        expected_error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": expected_error})
    return redirect(list_)
