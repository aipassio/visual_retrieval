from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('retrieval_insert', views.retrieval_insert, name='retrieval_insert'),
    path('retrieval_get', views.retrieval_get, name='retrieval_get')
]