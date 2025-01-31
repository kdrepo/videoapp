from django.urls import path
from . import views

from .views import (
    get_categories,
    get_topics,
    get_questions,
    get_youtube_links_by_category,
    get_youtube_links_by_topic,
    get_youtube_links_by_question,
    account_profile,
)

urlpatterns = [
    path('', views.table_of_contents, name='home'),
    path('chapter/<int:pk>/', views.chapter_detail, name='chapter_detail'),
    path('subheading/<int:pk>/', views.subheading_detail, name='subheading_detail'),
    # path('search/', views.search, name='search'),
    # path('toc/', views.toc, name='toc'),
    # Other URL patterns
    path('search-options/', views.search_options, name='search_options'),
    path('categories/', views.get_categories, name='get_categories'),
    path('youtube-links/<int:category_id>/', views.get_youtube_links_by_category, name='get_youtube_links_by_category'),
    path('searchall/', views.weighted_search, name='weighted_search'),

    path('topics/', get_topics, name='get_topics'),  # New route for topics
    path('questions/', get_questions, name='get_questions'),  # New route for questions
    path('youtube-links/topic/<str:topic_title>/', get_youtube_links_by_topic, name='get_youtube_links_by_topic'),  # New route for topics
    path('youtube-links/question/<str:question_text>/', get_youtube_links_by_question, name='get_youtube_links_by_question'),  # New route for questions
    path('profile/', account_profile, name='account_profile'),

]


