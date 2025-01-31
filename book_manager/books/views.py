

from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
from .models import Book, Chapter, Subheading, YouTubeLink, Category, Topic, Question
from django.http import JsonResponse


from django.shortcuts import render, get_object_or_404
from .models import Book, Chapter, Subheading, YouTubeLink, Category
from django.contrib.auth.decorators import login_required




@login_required
def account_profile(request):
    return render(request, 'account/profile.html', {'user': request.user})

def table_of_contents(request):
    # Fetch books and prefetch related chapters, subheadings, and their associated youtube_links
    books = Book.objects.prefetch_related(
        'chapters__subheadings',  # Prefetch subheadings related to each chapter
        # Prefetch youtube links associated with subheadings (correct related_name)
        'chapters__subheadings__youtube_links_subheading',
        # 'chapters__youtubelink_set',  # Prefetch youtube links associated with chapters (using the default related_name)
    )

    return render(request, 'books/table_of_contents.html', {'books': books})


def chapter_detail(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    return render(request, 'books/chapter_detail.html', {'chapter': chapter})


def subheading_detail(request, pk):
    subheading = get_object_or_404(Subheading, pk=pk)

    # Fetch YouTube links with their associated categories, topics, and questions
    youtube_links = subheading.youtube_links_subheading.prefetch_related('topics', 'questions')    

    return render(request, 'books/subheading_detail.html', {
        'subheading': subheading,
        'youtube_links': youtube_links,       
    })


def search_options(request):
    """
    Render the main page with search options.
    """
    return render(request, 'books/search_new.html')


def get_categories(request):
    """
    Fetch and return all categories.
    """
    categories = Category.objects.all().values('id', 'category')
    # print(categories)
    return JsonResponse({'categories': list(categories)})


def get_youtube_links_by_category(request, category_id):
    try:
        category = get_object_or_404(Category, id=category_id)
        youtube_links = category.youtube_links_categories.prefetch_related(
            'topics', 'questions', 'subheadings', 'categories')

        data = []
        for link in youtube_links:
            data.append({
                'id': link.id,
                'url': link.url,
                'title': link.title or "No Title",
                'description': link.description or "No Description",
                'embed_url_id': link.embed_url_id(),
                'topics': [{'topic': topic.topic_title, 'youtube_timestamp': topic.youtube_timestamp} for topic in link.topics.all()],
                'questions': [{'question_text': question.question_text, 'youtube_timestamp': question.youtube_timestamp} for question in link.questions.all()],
                'subheadings': [{'title': subheading.title, 'id': subheading.id} for subheading in link.subheadings.all()],
            })
        return JsonResponse({'youtube_links': data})
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)


def weighted_search(request):
    """
    Perform weighted full-text search based on topics, questions, or general text.
    """
    query = request.GET.get('query', '')
    search_type = request.GET.get(
        'search_type', 'topics')  # Default to text search
    results = []
    results_text_only = []

    if query:
        # Define search vectors for related fields
        topic_vector = SearchVector('topics__topic_title', weight='A')
        question_vector = SearchVector('questions__question_text', weight='A')
        search_vector_t = SearchVector(
            'title', weight='A') + SearchVector('text', weight='B')

        # Perform the search
        search_query = SearchQuery(query)

        # Determine the search vector
        if search_type == 'topics':
            search_vector = topic_vector
        elif search_type == 'questions':
            search_vector = question_vector
        elif search_type == 'general':
            search_vector = topic_vector + question_vector
        elif search_type == 'textonly':
            # Search Chapters
            chapters = Chapter.objects.annotate(
                rank=SearchRank(search_vector_t, search_query),
                headline=SearchHeadline(
                    'text',
                    search_query,
                    start_sel='<mark class="badge text-bg-warning">',
                    stop_sel='</mark>',
                    max_words=300,
                    min_words=50,
                ),
            ).filter(rank__gte=0.1).order_by('-rank')

            # Search Subheadings
            subheadings = Subheading.objects.annotate(
                rank=SearchRank(search_vector_t, search_query),
                headline=SearchHeadline(
                    'text',
                    search_query,
                    start_sel='<mark class="badge text-bg-warning">',
                    stop_sel='</mark>',
                    max_words=300,
                    min_words=50,
                ),
            ).filter(rank__gte=0.1).order_by('-rank')

            # Combine results for Chapters and Subheadings
            # for chapter in chapters:
            #     results_text_only.append({
            #         'type': 'chapter',
            #         'title': chapter.title,
            #         'text': chapter.text,
            #         'headline': chapter.headline,
            #         # 'youtube_links': list(chapter.youtube_links.all()),
            #         'breadcrumbs': f'Chapter: {chapter.title}'
            #     })
            for subheading in subheadings:
                results_text_only.append({
                    'type': 'subheading',
                    'id': subheading.id,
                    'title': subheading.title,
                    'text': subheading.text,
                    'headline': subheading.headline,
                    'youtube_links': list(subheading.youtube_links_subheading.all()),
                    'count': subheading.youtube_links_subheading.count(),
                    'breadcrumbs': f'Chapter: {subheading.chapter.title} > Subheading: {subheading.title}'
                })

            # Render results for 'onlytext' search
            # print(results_text_only)
            return render(
                request,
                'books/search_weighted.html',
                {'results_text_only': results_text_only,
                    'query': query, 'search_type': search_type},
            )
        else:
            # Handle invalid search_type
            return render(
                request,
                'books/search_weighted.html',
                {'error': 'Invalid search type',
                    'query': query, 'search_type': search_type},
            )

        # Process search results for other types
        matches = YouTubeLink.objects.annotate(
            rank=SearchRank(search_vector, search_query)
        ).filter(rank__gte=0.1).order_by('-rank')

        for match in matches:
            results.append({
                'match': match,
                'topics': match.topics.all(),
                'questions': match.questions.all(),
            })

    # Render results for non-'onlytext' search types
    return render(
        request,
        'books/search_weighted.html',
        {'results': results, 'query': query, 'search_type': search_type,
            'results_text_only': results_text_only},
    )


# def search(request):
#     query = request.GET.get('q')
#     results = []

#     if query:
#         # Build search vector and query
#         search_vector = SearchVector('title', weight='A') + SearchVector('text', weight='B')
#         search_query = SearchQuery(query)

#         # Search Chapters
#         chapters = Chapter.objects.annotate(
#             rank=SearchRank(search_vector, search_query),
#             headline=SearchHeadline('text', search_query, start_sel='<mark class="badge text-bg-success">', stop_sel='</b>', max_words=300, min_words=50)
#         ).filter(rank__gte=0.1).order_by('-rank')

#         # Search Subheadings
#         subheadings = Subheading.objects.annotate(
#             rank=SearchRank(search_vector, search_query),
#             headline=SearchHeadline('text', search_query, start_sel='<mark class="badge text-bg-success">', stop_sel='</b>''</mark>', max_words=300, min_words=50)
#         ).filter(rank__gte=0.1).order_by('-rank')

#         # Combine results with YouTube links
#         for chapter in chapters:
#             results.append({
#                 'type': 'chapter',
#                 'title': chapter.title,
#                 'text': chapter.text,
#                 'headline': chapter.headline,
#                 'youtube_links': list(chapter.youtube_links.all()),
#                 'breadcrumbs': f'Chapter: {chapter.title}'
#             })
#         for subheading in subheadings:
#             results.append({
#                 'type': 'subheading',
#                 'id': subheading.id,
#                 'title': subheading.title,
#                 'text': subheading.text,
#                 'headline': subheading.headline,
#                 'youtube_links': list(subheading.youtube_links.all()),
#                 'breadcrumbs': f'Chapter: {subheading.chapter.title} > Subheading: {subheading.title}'
#             })

#     return render(request, 'books/search_results.html', {'results': results, 'query': query})




def get_topics(request):
    """
    Fetch and return all unique topics.
    """
    topics = Topic.objects.values_list('topic_title', flat=True).distinct()
    return JsonResponse({'topics': list(topics)})

def get_questions(request):
    """
    Fetch and return all unique questions.
    """
    questions = Question.objects.values_list('question_text', flat=True).distinct()
    return JsonResponse({'questions': list(questions)})

def get_youtube_links_by_topic(request, topic_title):
    """
    Fetch and return all YouTube links related to a specific topic.
    """
    youtube_links = YouTubeLink.objects.filter(topics__topic_title=topic_title).prefetch_related('topics', 'questions', 'subheadings', 'categories')
    data = []
    for link in youtube_links:
        data.append({
            'id': link.id,
            'url': link.url,
            'title': link.title or "No Title",
            'description': link.description or "No Description",
            'embed_url_id': link.embed_url_id(),
            'topics': [{'topic': topic.topic_title, 'youtube_timestamp': topic.youtube_timestamp} for topic in link.topics.all()],
            'questions': [{'question_text': question.question_text, 'youtube_timestamp': question.youtube_timestamp} for question in link.questions.all()],
            'subheadings': [{'title': subheading.title, 'id': subheading.id} for subheading in link.subheadings.all()],
        })
    return JsonResponse({'youtube_links': data})

def get_youtube_links_by_question(request, question_text):
    """
    Fetch and return all YouTube links related to a specific question.
    """
    youtube_links = YouTubeLink.objects.filter(questions__question_text=question_text).prefetch_related('topics', 'questions', 'subheadings', 'categories')
    data = []
    for link in youtube_links:
        data.append({
            'id': link.id,
            'url': link.url,
            'title': link.title or "No Title",
            'description': link.description or "No Description",
            'embed_url_id': link.embed_url_id(),
            'topics': [{'topic': topic.topic_title, 'youtube_timestamp': topic.youtube_timestamp} for topic in link.topics.all()],
            'questions': [{'question_text': question.question_text, 'youtube_timestamp': question.youtube_timestamp} for question in link.questions.all()],
            'subheadings': [{'title': subheading.title, 'id': subheading.id} for subheading in link.subheadings.all()],
        })
    return JsonResponse({'youtube_links': data})
