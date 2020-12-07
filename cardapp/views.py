from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from accounts.models import CustomUser
from smarturlprj.settings import ALLOWED_HOSTS

# Create your views here.
def index(request):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    context = {'host': host}
    return render(request, 'index.html', context)

def create_links(request, username):

    #owner = CustomUser.objects.get(username=username)
    owner = get_object_or_404(CustomUser, username=username)
    if not owner:
        return redirect('index')

    bg = Background.objects.filter(user=owner)
    blocks = CreateBlock.objects.filter(user=owner)
    links = CreateLink.objects.filter(user=owner)
    faqs = CreateFaq.objects.filter(user=owner)
    tablescat = TableCategory.objects.filter(user=owner)
    tablesitem = TableItems.objects.filter(user=owner)
    imgs = AddImage.objects.filter(user=owner)
    vid = YoutubeVideo.objects.filter(user=owner)
    #profile = CardProfile.objects.all()

    context = {'links': links,
               'blocks': blocks,
               'faqs': faqs,
               'tablescat': tablescat,
               'tablesitem': tablesitem,
               'imgs': imgs,
               'vid': vid,
               'bg': bg,
               'owner': owner,
               }

    return render(request, 'card.html', context)

