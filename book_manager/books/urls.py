from django.urls import path
from . import views

urlpatterns = [
    path('', views.table_of_contents, name='table_of_contents'),
    path('chapter/<int:pk>/', views.chapter_detail, name='chapter_detail'),
    path('subheading/<int:pk>/', views.subheading_detail, name='subheading_detail'),
    # path('subheading/<int:pk>/', views.subheading_detail, name='subheading_detail'),
    # path('search/', views.search, name='search'),
]
