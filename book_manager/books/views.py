from django.shortcuts import render, get_object_or_404

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
from django.shortcuts import render
from .models import Book, Chapter, Subheading, YouTubeLink



# def table_of_contents(request):
#     books = Book.objects.prefetch_related(
#         'chapters__subheadings__subheadings2',
#         'chapters__youtube_links',
#         'chapters__subheadings__youtube_links',
#         'chapters__subheadings__subheadings2__youtube_links',
#     )
#     return render(request, 'books/table_of_contents.html', {'books': books})


# def chapter_detail(request, pk):
#     chapter = get_object_or_404(Chapter, pk=pk)
#     return render(request, 'books/chapter_detail.html', {'chapter': chapter})


# def subheading_detail(request, pk):
#     subheading = get_object_or_404(Subheading, pk=pk)
#     return render(request, 'books/subheading_detail.html', {'subheading': subheading})

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
#             headline=SearchHeadline('text', search_query, start_sel='<b>', stop_sel='</b>')
#         ).filter(rank__gte=0.1).order_by('-rank')

#         # Search Subheadings
#         subheadings = Subheading.objects.annotate(
#             rank=SearchRank(search_vector, search_query),
#             headline=SearchHeadline('text', search_query, start_sel='<b>', stop_sel='</b>', max_words=300, min_words=50)
#         ).filter(rank__gte=0.1).order_by('-rank')

#         # Search Subheading2s
#         subheading2s = Subheading2.objects.annotate(
#             rank=SearchRank(search_vector, search_query),
#             headline=SearchHeadline('text', search_query, start_sel='<b>', stop_sel='</b>')
#         ).filter(rank__gte=0.1).order_by('-rank')

#         # Combine results with YouTube links and breadcrumbs
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
#                 '4link': 'Subhead Title',
#                 'type': 'subheading_detail',
#                 'id': subheading.id,
#                 'title': subheading.title,
#                 'text': subheading.text,
#                 'headline': subheading.headline,
#                 'youtube_links': list(subheading.youtube_links.all()),
#                 'breadcrumbs': f'Chapter: {subheading.chapter.title} > Subheading: {subheading.title}'
#             })
#         for subheading2 in subheading2s:
#             results.append({
#                 'type': 'Subheading2',
#                 'title': subheading2.title,
#                 'text': subheading2.text,
#                 'headline': subheading2.headline,
#                 'youtube_links': list(subheading2.youtube_links.all()),
#                 'breadcrumbs': f'Chapter: {subheading2.subheading.chapter.title} > Subheading: {subheading2.subheading.title} > Subheading2: {subheading2.title}'
#             })

#     return render(request, 'books/search_results.html', {'results': results, 'query': query})


from django.shortcuts import render, get_object_or_404
from .models import Book, Chapter, Subheading, YouTubeLink


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

