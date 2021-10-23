from django.shortcuts import render, redirect
from django.http import HttpResponse
from list.models import Item

# Create your views here.
def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-pnly-list-in-the-world')

    items = Item.objects.all()

    return render(request,'home.html',{'items':items})
