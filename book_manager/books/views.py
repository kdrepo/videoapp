from django.shortcuts import render, get_object_or_404

from .models import Book, Chapter, Subheading

from django.shortcuts import render



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


