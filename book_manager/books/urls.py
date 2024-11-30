from django.urls import path
from . import views

urlpatterns = [
    path('', views.table_of_contents, name='home'),
    path('chapter/<int:pk>/', views.chapter_detail, name='chapter_detail'),
    path('subheading/<int:pk>/', views.subheading_detail, name='subheading_detail'),
    path('search/', views.search, name='search'),
    # path('toc/', views.toc, name='toc'),
    # Other URL patterns
    path('search-options/', views.search_options, name='search_options'),
    path('categories/', views.get_categories, name='get_categories'),
    path('youtube-links/<int:category_id>/', views.get_youtube_links_by_category, name='get_youtube_links_by_category'),
    path('searchall/', views.weighted_search, name='weighted_search'),
]
