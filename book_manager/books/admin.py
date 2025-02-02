# from django.contrib import admin
# from .models import Book, Chapter, Subheading, YouTubeLink, Category, Topic, Question


# # # Admin for Book model
# # class BookAdmin(admin.ModelAdmin):
# #     """Admin configuration for Book model."""
# #     list_display = ['id', 'title', 'author']
# #     search_fields = ['title', 'author']
# #     ordering = ['id']  # Default ordering by ID


# # # Admin for Chapter model (Related to Book)
# # class ChapterAdmin(admin.ModelAdmin):
# #     """Admin configuration for Chapter model."""
# #     list_display = ['id', 'title', 'book', 'text']
# #     list_filter = ['book']
# #     search_fields = ['title', 'text']
# #     ordering = ['id']  # Default ordering by ID


# # # Admin for Subheading model (Related to Chapter)
# # class SubheadingAdmin(admin.ModelAdmin):
# #     """Admin configuration for Subheading model."""
# #     list_display = ['id', 'title', 'chapter', 'text']
# #     list_filter = ['chapter']
# #     search_fields = ['title', 'text']
# #     ordering = ['id']  # Default ordering by ID


# # # Admin for Category model
# # class CategoryAdmin(admin.ModelAdmin):
# #     """Admin configuration for Category model."""
# #     list_display = ['category']
# #     search_fields = ['category']
# #     ordering = ['id']  # Default ordering by ID


# # # Admin for Topic model (Related to YouTubeLink)
# # class TopicAdmin(admin.ModelAdmin):
# #     """Admin configuration for Topic model."""
# #     list_display = ['id', 'topic_title', 'youtube_timestamp']
# #     search_fields = ['topic_title']
# #     ordering = ['topic_title']  # Default ordering by topic_title


# # # Admin for Question model (Related to YouTubeLink)
# # class QuestionAdmin(admin.ModelAdmin):
# #     """Admin configuration for Question model."""
# #     list_display = ['id', 'question_text', 'youtube_timestamp']
# #     search_fields = ['question_text']
# #     ordering = ['id']  # Default ordering by ID


# # # Admin for YouTubeLink model (Related to Subheading, Topic, and Question)
# # class YouTubeLinkAdmin(admin.ModelAdmin):
# #     """Admin configuration for YouTubeLink model."""
# #     list_display = ['id', 'url', 'title', 'description', 'display_subheadings', 'display_topics', 'display_questions']
# #     search_fields = ['url', 'description']
# #     filter_horizontal = ['subheadings', 'topics', 'questions']  # For Many-to-Many relationships
# #     ordering = ['id']  # Default ordering by ID

# #     # Display related subheadings in a comma-separated list
# #     def display_subheadings(self, obj):
# #         """Display all related subheadings."""
# #         return ", ".join([subheading.title for subheading in obj.subheadings.all()])
# #     display_subheadings.short_description = 'Subheadings'

# #     # Display related topics in a comma-separated list
# #     def display_topics(self, obj):
# #         """Display all related topics."""
# #         return ", ".join([topic.topic_title for topic in obj.topics.all()])
# #     display_topics.short_description = 'Topics'

# #     # Display related questions in a comma-separated list
# #     def display_questions(self, obj):
# #         """Display all related questions."""
# #         return ", ".join([question.question_text[:50] for question in obj.questions.all()])
# #     display_questions.short_description = 'Questions'


# # Registering the models with the admin interface
# # admin.site.register(Book)
# # admin.site.register(Chapter)
# # admin.site.register(Subheading)
# # admin.site.register(Category)
# # admin.site.register(Topic)
# # admin.site.register(Question)
# # admin.site.register(YouTubeLink)



# from django.contrib import admin
# from .models import Book, Chapter, Subheading, YouTubeLink, Category, Topic, Question
# from import_export.admin import ImportExportModelAdmin


# class bookixAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     ...

# class chapixAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     ...

# class subixAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     ...
# class catixAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     ...
# class topicixAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     ...
# class questionixAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     ...
# class youtubelinkixAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     ...



# # Admin for Book model
# class BookAdmin(bookixAdmin, admin.ModelAdmin):
#     """Admin configuration for Book model."""
#     list_display = ['id', 'title', 'author']
#     search_fields = ['title', 'author']
#     ordering = ['id']  # Default ordering by ID


# # Admin for Chapter model (Related to Book)
# class ChapterAdmin(chapixAdmin, admin.ModelAdmin):
#     """Admin configuration for Chapter model."""
#     list_display = ['id', 'title', 'book']
#     list_filter = ['book']
#     search_fields = ['title', 'text']
#     ordering = ['id']  # Default ordering by ID


# # Admin for Subheading model (Related to Chapter)
# class SubheadingAdmin(subixAdmin, admin.ModelAdmin):
#     """Admin configuration for Subheading model."""
#     list_display = ['id', 'title', 'chapter']
#     list_filter = ['chapter']
#     search_fields = ['title', 'text']
#     ordering = ['id']  # Default ordering by ID


# # Admin for Category model
# class CategoryAdmin(catixAdmin, admin.ModelAdmin):
#     """Admin configuration for Category model."""
#     list_display = ['category']
#     search_fields = ['category']
#     ordering = ['id']  # Default ordering by ID


# # Admin for Topic model
# class TopicAdmin(topicixAdmin, admin.ModelAdmin):
#     """Admin configuration for Topic model."""
    
#     # Custom method to display associated YouTube Links for the topic
#     def youtube_links_topic(self, obj):
#         return ", ".join([link.url for link in obj.youtube_link.all()])  # Display URLs of associated YouTube Links
    
#     youtube_links_topic.short_description = 'YouTube Links'  # Change the column name in the list view

#     # Admin configuration
#     list_display = ['youtube_links_topic', 'topic_title', 'youtube_timestamp']
#     search_fields = ['topic_title']
#     filter_horizontal = ['youtube_link']  # For Many-to-Many relationships
#     ordering = ['topic_title']  # Default ordering by topic_title


# # Admin for Question model
# class QuestionAdmin(questionixAdmin, admin.ModelAdmin):
#     """Admin configuration for Question model."""
    
#     # Custom method to display associated YouTube Links for the question
#     def youtube_links_question(self, obj):
#         return ", ".join([link.url for link in obj.youtube_link.all()])  # Display URLs of associated YouTube Links
    
#     youtube_links_question.short_description = 'YouTube Links'  # Change the column name in the list view

#     # Admin configuration
#     list_display = ['youtube_links_question', 'question_text', 'youtube_timestamp']
#     filter_horizontal = ['youtube_link']  # For Many-to-Many relationships
#     search_fields = ['question_text']
#     ordering = ['id']  # Default ordering by ID


# # Admin for YouTubeLink model (Related to Subheading, Topic, and Question)
# class YouTubeLinkAdmin(youtubelinkixAdmin, admin.ModelAdmin):
#     """Admin configuration for YouTubeLink model."""
#     list_display = ['id', 'title', 'display_subheadings', 'display_topics', 'display_questions']
#     search_fields = ['url', 'description']
#     filter_horizontal = ['subheadings', 'topics', 'questions', 'categories']  # For Many-to-Many relationships
#     ordering = ['id']  # Default ordering by ID

#     # Display related subheadings in a comma-separated list
#     def display_subheadings(self, obj):
#         """Display all related subheadings."""
#         return ", ".join([subheading.title for subheading in obj.subheadings.all()])
#     display_subheadings.short_description = 'Subheadings'

#     # Display related topics in a comma-separated list
#     def display_topics(self, obj):
#         """Display all related topics."""
#         return ", ".join([topic.topic_title for topic in obj.topics.all()])
#     display_topics.short_description = 'Topics'

#     # Display related questions in a comma-separated list
#     def display_questions(self, obj):
#         """Display all related questions."""
#         return ", ".join([question.question_text[:50] for question in obj.questions.all()])
#     display_questions.short_description = 'Questions'


# # Register models with their corresponding admin configurations
# admin.site.register(Book, BookAdmin)
# admin.site.register(Chapter, ChapterAdmin)
# admin.site.register(Subheading, SubheadingAdmin)
# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Topic, TopicAdmin)
# admin.site.register(Question, QuestionAdmin)
# admin.site.register(YouTubeLink, YouTubeLinkAdmin)



from django.contrib import admin
from .models import Book, Chapter, Subheading, YouTubeLink, Category, Topic, Question, Profile
from import_export.admin import ImportExportModelAdmin

# Base Admin Classes
class BaseImportExportAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass

# Admin for Book model
class BookAdmin(BaseImportExportAdmin):
    list_display = ['id', 'title', 'author']
    search_fields = ['title', 'author']
    ordering = ['id']

# Admin for Chapter model (Related to Book)
class ChapterAdmin(BaseImportExportAdmin):
    list_display = ['id', 'title', 'book']
    list_filter = ['book']
    search_fields = ['title', 'text']
    ordering = ['id']

# Admin for Subheading model (Related to Chapter)
class SubheadingAdmin(BaseImportExportAdmin):
    list_display = ['id', 'title', 'chapter']
    list_filter = ['chapter']
    search_fields = ['title', 'text']
    ordering = ['id']

# Admin for Category model
class CategoryAdmin(BaseImportExportAdmin):
    list_display = ['id', 'category']
    search_fields = ['category']
    ordering = ['id']

# Admin for Topic model
class TopicAdmin(BaseImportExportAdmin):
    list_display = ['id', 'topic_title', 'youtube_link', 'youtube_timestamp']
    search_fields = ['topic_title']
    ordering = ['topic_title']

# Admin for Question model
class QuestionAdmin(BaseImportExportAdmin):
    list_display = ['id', 'question_text', 'youtube_timestamp']
    search_fields = ['question_text']
    ordering = ['id']

# Admin for YouTubeLink model
class YouTubeLinkAdmin(BaseImportExportAdmin):
    list_display = ['id', 'url', 'title', 'description', 'display_subheadings']
    search_fields = ['url', 'description']
    ordering = ['id']

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
admin.site.register(Profile)