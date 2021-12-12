from django.shortcuts import render, redirect
from django.http import HttpResponse
from list.models import Item, List

# Create your views here.
def home_page(request):
    # if request.method == 'POST':
    #     Item.objects.create(text=request.POST['item_text'])
    #     return redirect('/lists/the-only-list-in-the-world')
    #
    # # items = Item.objects.all()

    return render(request,'home.html')

def view_list(request, list_id):
    list_=List.objects.get(id=list_id)
    # items=Item.objects.filter(list=list_)
    return render(request,'list.html',{'list':list_})

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))


# def new_list(request):
#     list_=List.objects.create()
#     Item.objects.create(text=request.POST['item_text'],list=list_)
#     return redirect(f'/lists/{list_.id}/')
    # items = Item.objects.all

def add_item(request, list_id):
    list_=List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'],list=list_)
    return redirect(f'/lists/{list_.id}/')
