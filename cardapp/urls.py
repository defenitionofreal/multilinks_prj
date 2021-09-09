from django.urls import path
from . import views

app_name = 'cardapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:username>/', views.create_links, name='create_links'),
    # api's
    path("block/", views.BlockView.as_view()),
]