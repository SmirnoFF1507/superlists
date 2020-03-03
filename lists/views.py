from django.shortcuts import redirect, render
from lists.models import Item, List

def home_page(request):
    '''домашняя страница'''
    return render(request, 'home.html')

def view_list(request):
    '''новый список'''
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})

def new_list(request):
    '''новый список'''
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/one_list_in_world/')
