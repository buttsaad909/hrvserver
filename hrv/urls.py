from django.urls import path

from . import views

urlpatterns = [
    path('', views.post, name='index'),
    path('page', views.page, name="page"),
    path('page2', views.page2, name="page2")
]