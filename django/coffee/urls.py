from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    # path ('<slug:category_slug>/', views.home, name='index'),

]