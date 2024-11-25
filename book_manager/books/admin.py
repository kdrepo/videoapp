from django.contrib import admin
from .models import Book, Chapter, Subheading, YouTubeLink, Category, Topic, Question


class YouTubeLinkInline(admin.TabularInline):
    """Inline form for managing YouTube links with Chapters."""
    model = YouTubeLink.chapters.through  # Many-to-Many intermediary table for Chapters
    extra = 1  # Number of empty forms to display
    verbose_name = "Chapter-YouTube Link Association"
    verbose_name_plural = "Chapter-YouTube Link Associations"


class YouTubeLinkSubheadingInline(admin.TabularInline):
    """Inline form for managing YouTube links with Subheadings."""
    model = YouTubeLink.subheadings.through  # Many-to-Many intermediary table for Subheadings
    extra = 1
    verbose_name = "Subheading-YouTube Link Association"
    verbose_name_plural = "Subheading-YouTube Link Associations"


class ChapterAdmin(admin.ModelAdmin):
    """Admin configuration for Chapter model."""
    list_display = ['id', 'title', 'book', 'order']
    list_filter = ['book']
    search_fields = ['title', 'text']
    inlines = [YouTubeLinkInline]  # Add inline for Chapters


class SubheadingAdmin(admin.ModelAdmin):
    """Admin configuration for Subheading model."""
    list_display = ['id', 'title', 'chapter', 'order']
    list_filter = ['chapter']
    search_fields = ['title', 'text']
    inlines = [YouTubeLinkSubheadingInline]  # Add inline for Subheadings
    ordering = ['-id']


class BookAdmin(admin.ModelAdmin):
    """Admin configuration for Book model."""
    list_display = ['id', 'title', 'author']
    search_fields = ['title', 'author']
    ordering = ['title']


class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""
    list_display = ['category']
    search_fields = ['category']
    ordering = ['category']


class TopicAdmin(admin.ModelAdmin):
    """Admin configuration for Topic model."""
    list_display = ['topic', 'youtube_timestamp']
    search_fields = ['topic']
    ordering = ['topic']


class QuestionAdmin(admin.ModelAdmin):
    """Admin configuration for Question model."""
    list_display = ['question_text']
    search_fields = ['question_text']
    ordering = ['id']


class YouTubeLinkAdmin(admin.ModelAdmin):
    """Admin configuration for YouTubeLink model."""
    list_display = ['id', 'url', 'description', 'display_categories', 'display_topics', 'display_questions', 'display_chapters', 'display_subheadings']
    search_fields = ['url', 'description']
    filter_horizontal = ['categories', 'topics', 'questions', 'chapters', 'subheadings']

    def display_categories(self, obj):
        """Display all related categories."""
        return ", ".join([category.category for category in obj.categories.all()])
    display_categories.short_description = 'Categories'

    def display_topics(self, obj):
        """Display all related topics."""
        return ", ".join([topic.topic for topic in obj.topics.all()])
    display_topics.short_description = 'Topics'

    def display_questions(self, obj):
        """Display all related questions."""
        return ", ".join([question.question_text[:50] for question in obj.questions.all()])
    display_questions.short_description = 'Questions'

    def display_chapters(self, obj):
        """Display all related chapters."""
        return ", ".join([chapter.title for chapter in obj.chapters.all()])
    display_chapters.short_description = 'Chapters'

    def display_subheadings(self, obj):
        """Display all related subheadings."""
        return ", ".join([subheading.title for subheading in obj.subheadings.all()])
    display_subheadings.short_description = 'Subheadings'


# Register models with their corresponding admin configurations
admin.site.register(Book, BookAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Subheading, SubheadingAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(YouTubeLink, YouTubeLinkAdmin)
