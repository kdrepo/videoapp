from django.shortcuts import render, get_object_or_404

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.shortcuts import render
from .models import Book, Chapter, Subheading, Subheading2, YouTubeLink



def table_of_contents(request):
    books = Book.objects.prefetch_related(
        'chapters__subheadings__subheadings2',
        'chapters__youtube_links',
        'chapters__subheadings__youtube_links',
        'chapters__subheadings__subheadings2__youtube_links',
    )
    return render(request, 'books/table_of_contents.html', {'books': books})


def chapter_detail(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    return render(request, 'books/chapter_detail.html', {'chapter': chapter})


def subheading_detail(request, pk):
    subheading = get_object_or_404(Subheading, pk=pk)
    return render(request, 'books/subheading_detail.html', {'subheading': subheading})


# def search(request):
#     query = request.GET.get('q')
#     results = []

#     if query:
#         # Perform search on all three models
#         search_vector = SearchVector('title', 'text')
#         search_query = SearchQuery(query)

#         chapters = Chapter.objects.annotate(
#             rank=SearchRank(search_vector, search_query)
#         ).filter(rank__gte=0.1).order_by('-rank')
#         print(chapters)

#         subheadings = Subheading.objects.annotate(
#             rank=SearchRank(search_vector, search_query)
#         ).filter(rank__gte=0.1).order_by('-rank')
#         print(subheadings)

#         subheading2s = Subheading2.objects.annotate(
#             rank=SearchRank(search_vector, search_query)
#         ).filter(rank__gte=0.1).order_by('-rank')

#         # Combine results with YouTube links and breadcrumbs
#         for chapter in chapters:
#             results.append({
#                 'type': 'Chapter',
#                 'title': chapter.title,
#                 'text': chapter.text,
#                 'youtube_links': chapter.youtube_links.all(),
#                 'breadcrumbs': f'Chapter: {chapter.title}'
#             })
#         for subheading in subheadings:
#             results.append({
#                 'type': 'Subheading',
#                 'title': subheading.title,
#                 'text': subheading.text,
#                 'youtube_links': subheading.youtube_links.all(),
#                 'breadcrumbs': f'Chapter: {subheading.chapter.title} > Subheading: {subheading.title}'
#             })
#         for subheading2 in subheading2s:
#             results.append({
#                 'type': 'Subheading2',
#                 'title': subheading2.title,
#                 'text': subheading2.text,
#                 'youtube_links': subheading2.youtube_links.all(),
#                 'breadcrumbs': f'Chapter: {subheading2.subheading.chapter.title} > Subheading: {subheading2.subheading.title} > Subheading2: {subheading2.title}'
#             })
#     print(results)
#     return render(request, 'books/search_results.html', {'results': results, 'query': query})



from django.shortcuts import render
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .models import Chapter, Subheading, Subheading2
# import logging

# logger = logging.getLogger(__name__)

# def search(request):
#     query = request.GET.get('q')
#     results = []

#     if query:
#         # Build search vector and query
#         search_vector = SearchVector('title', weight='A') + SearchVector('text', weight='B')
#         search_query = SearchQuery(query)

#         # Search Chapters
#         chapters = Chapter.objects.annotate(
#             rank=SearchRank(search_vector, search_query)
#         ).filter(rank__gte=0.1).order_by('-rank')
#         # logger.debug(f"Chapters Query: {chapters.query}")
#         # logger.debug(f"Chapters Results: {list(chapters)}")
#         # print(chapters)

#         # Search Subheadings
#         subheadings = Subheading.objects.annotate(
#             rank=SearchRank(search_vector, search_query)
#         ).filter(rank__gte=0.1).order_by('-rank')
#         # logger.debug(f"Subheadings Results: {list(subheadings)}")

#         # Search Subheading2s
#         subheading2s = Subheading2.objects.annotate(
#             rank=SearchRank(search_vector, search_query)
#         ).filter(rank__gte=0.1).order_by('-rank')
#         # logger.debug(f"Subheading2s Results: {list(subheading2s)}")

#         # Combine results with YouTube links and breadcrumbs
#         for chapter in chapters:
#             results.append({
#                 'type': 'Chapter',
#                 'title': chapter.title,
#                 'text': chapter.text,
#                 'youtube_links': list(chapter.youtube_links.all()),
#                 'breadcrumbs': f'Chapter: {chapter.title}'
#             })
#         for subheading in subheadings:
#             results.append({
#                 'type': 'Subheading',
#                 'title': subheading.title,
#                 'text': subheading.text,
#                 'youtube_links': list(subheading.youtube_links.all()),
#                 'breadcrumbs': f'Chapter: {subheading.chapter.title} > Subheading: {subheading.title}'
#             })
#         for subheading2 in subheading2s:
#             results.append({
#                 'type': 'Subheading2',
#                 'title': subheading2.title,
#                 'text': subheading2.text,
#                 'youtube_links': list(subheading2.youtube_links.all()),
#                 'breadcrumbs': f'Chapter: {subheading2.subheading.chapter.title} > Subheading: {subheading2.subheading.title} > Subheading2: {subheading2.title}'
#             })

#     # logger.debug(f"Final Results: {results}")
#     return render(request, 'books/search_results.html', {'results': results, 'query': query})












from django.contrib.postgres.search import (
    SearchVector, SearchQuery, SearchRank, SearchHeadline
)
from django.shortcuts import render
from .models import Chapter, Subheading, Subheading2

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
            headline=SearchHeadline('text', search_query, start_sel='<b>', stop_sel='</b>')
        ).filter(rank__gte=0.1).order_by('-rank')

        # Search Subheadings
        subheadings = Subheading.objects.annotate(
            rank=SearchRank(search_vector, search_query),
            headline=SearchHeadline('text', search_query, start_sel='<b>', stop_sel='</b>', max_words=300, min_words=50)
        ).filter(rank__gte=0.1).order_by('-rank')

        # Search Subheading2s
        subheading2s = Subheading2.objects.annotate(
            rank=SearchRank(search_vector, search_query),
            headline=SearchHeadline('text', search_query, start_sel='<b>', stop_sel='</b>')
        ).filter(rank__gte=0.1).order_by('-rank')

        # Combine results with YouTube links and breadcrumbs
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
                '4link': 'Subhead Title',
                'type': 'subheading_detail',
                'id': subheading.id,
                'title': subheading.title,
                'text': subheading.text,
                'headline': subheading.headline,
                'youtube_links': list(subheading.youtube_links.all()),
                'breadcrumbs': f'Chapter: {subheading.chapter.title} > Subheading: {subheading.title}'
            })
        for subheading2 in subheading2s:
            results.append({
                'type': 'Subheading2',
                'title': subheading2.title,
                'text': subheading2.text,
                'headline': subheading2.headline,
                'youtube_links': list(subheading2.youtube_links.all()),
                'breadcrumbs': f'Chapter: {subheading2.subheading.chapter.title} > Subheading: {subheading2.subheading.title} > Subheading2: {subheading2.title}'
            })

    return render(request, 'books/search_results.html', {'results': results, 'query': query})
