from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
from .models import Book, Chapter, Subheading, YouTubeLink, Category
from django.http import JsonResponse



def table_of_contents(request):
    books = Book.objects.prefetch_related(
        'chapters__subheadings',
        'chapters__youtube_links',
        'chapters__subheadings__youtube_links',
    )
    return render(request, 'books/table_of_contents.html', {'books': books})


def chapter_detail(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    return render(request, 'books/chapter_detail.html', {'chapter': chapter})


def subheading_detail(request, pk):
    subheading = get_object_or_404(Subheading, pk=pk)

    # Fetch YouTube links with their associated categories, topics, and questions
    youtube_links = subheading.youtube_links.prefetch_related('categories', 'topics', 'questions')

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
    return JsonResponse({'categories': list(categories)})


def get_youtube_links_by_category(request, category_id):
    """
    Fetch and return YouTube links for a specific category, including subheadings.
    """
    try:
        category = get_object_or_404(Category, id=category_id)
        youtube_links = category.youtube_links.prefetch_related('topics', 'questions', 'categories', 'subheadings')

        data = []
        for link in youtube_links:
            data.append({
                'id': link.id,
                'url': link.url,
                'title': link.title or "No Title",
                'description': link.description or "No Description",
                'embed_url_id': link.embed_url_id(),
                'topics': [topic.topic for topic in link.topics.all()],
                'questions': [question.question_text for question in link.questions.all()],
                'subheadings': [subheading.title for subheading in link.subheadings.all()],
            })
        return JsonResponse({'youtube_links': data})
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)
    




def weighted_search(request):
    """
    Perform weighted full-text search based on topics, questions, or general text.
    """
    query = request.GET.get('query', '')
    search_type = request.GET.get('search_type', 'text')  # Default to text search
    results = []

    if query:
        # Define search vectors for related fields
        topic_vector = SearchVector('topics__topic', weight='A')
        question_vector = SearchVector('questions__question_text', weight='A')

        # Determine the search vector
        if search_type == 'topics':
            search_vector = topic_vector
        elif search_type == 'questions':
            search_vector = question_vector
        else:
            search_vector = topic_vector + question_vector

        # Perform the search
        search_query = SearchQuery(query)
        matches = YouTubeLink.objects.annotate(
            rank=SearchRank(search_vector, search_query)
        ).filter(rank__gte=0.1).order_by('-rank')

        # Debug the SQL query
        # print(matches.query)

        # Process results for rendering
        for match in matches:
            results.append({
                'match': match,
                'topics': match.topics.all(),
                'questions': match.questions.all(),
            })
    print(results)
    return render(request, 'books/search_weighted.html', {'results': results, 'query': query, 'search_type': search_type})




def search(request):
    query = request.GET.get('q')
    results = []

    if query:
        # Build search vector and query
        search_vector = SearchVector('title', weight='A') + SearchVector('text', weight='B')
        search_query = SearchQuery(query)

        # Search Chapters
        chapters = Chapter.objects.annotate(
            rank=SearchRank(search_vector, search_query),
            headline=SearchHeadline('text', search_query, start_sel='<mark class="badge text-bg-success">', stop_sel='</b>', max_words=300, min_words=50)
        ).filter(rank__gte=0.1).order_by('-rank')

        # Search Subheadings
        subheadings = Subheading.objects.annotate(
            rank=SearchRank(search_vector, search_query),
            headline=SearchHeadline('text', search_query, start_sel='<mark class="badge text-bg-success">', stop_sel='</b>''</mark>', max_words=300, min_words=50)
        ).filter(rank__gte=0.1).order_by('-rank')

        # Combine results with YouTube links
        for chapter in chapters:
            results.append({
                'type': 'chapter',
                'title': chapter.title,
                'text': chapter.text,
                'headline': chapter.headline,
                'youtube_links': list(chapter.youtube_links.all()),
                'breadcrumbs': f'Chapter: {chapter.title}'
            })
        for subheading in subheadings:
            results.append({
                'type': 'subheading',
                'id': subheading.id,
                'title': subheading.title,
                'text': subheading.text,
                'headline': subheading.headline,
                'youtube_links': list(subheading.youtube_links.all()),
                'breadcrumbs': f'Chapter: {subheading.chapter.title} > Subheading: {subheading.title}'
            })

    return render(request, 'books/search_results.html', {'results': results, 'query': query})