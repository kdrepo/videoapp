from django.contrib import admin
from .models import Book, Chapter, Subheading, Subheading2, YouTubeLink


class YouTubeLinkInline(admin.TabularInline):
    """Inline form for adding YouTube links."""
    model = YouTubeLink
    extra = 1  # Number of empty forms to display
    fields = ['url', 'description']
    verbose_name = "YouTube Link"
    verbose_name_plural = "YouTube Links"


class ChapterAdmin(admin.ModelAdmin):
    """Admin configuration for Chapter model."""
    list_display = ['title', 'book', 'order']
    list_filter = ['book']
    search_fields = ['title', 'text']
    inlines = [YouTubeLinkInline]
    ordering = ['book', 'order']


class SubheadingAdmin(admin.ModelAdmin):
    """Admin configuration for Subheading model."""
    list_display = ['title', 'chapter', 'order']
    list_filter = ['chapter']
    search_fields = ['title', 'text']
    inlines = [YouTubeLinkInline]
    ordering = ['chapter', 'order']


class Subheading2Admin(admin.ModelAdmin):
    """Admin configuration for Subheading2 model."""
    list_display = ['title', 'subheading', 'order']
    list_filter = ['subheading']
    search_fields = ['title', 'text']
    inlines = [YouTubeLinkInline]
    ordering = ['subheading', 'order']


class BookAdmin(admin.ModelAdmin):
    """Admin configuration for Book model."""
    list_display = ['title', 'author']
    search_fields = ['title', 'author']
    ordering = ['title']


# Register models with their corresponding admin configurations
admin.site.register(Book, BookAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Subheading, SubheadingAdmin)
admin.site.register(Subheading2, Subheading2Admin)
admin.site.register(YouTubeLink)
