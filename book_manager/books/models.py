from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.db.models import Index


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']  # Default ordering by ID in ascending order

    def __str__(self):
        return self.title


class Chapter(models.Model):
    book = models.ForeignKey(Book, related_name="chapters", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)
    search_vector = SearchVectorField(null=True, blank=True)  # For full-text search

    class Meta:
        indexes = [
            Index(fields=["search_vector"]),
        ]
        ordering = ['id']  # Default ordering by ID in ascending order

    def __str__(self):
        return f"{self.book.title} - {self.title}"


class Subheading(models.Model):
    chapter = models.ForeignKey(Chapter, related_name="subheadings", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)
    search_vector = SearchVectorField(null=True, blank=True)  # For full-text search

    class Meta:
        indexes = [
            Index(fields=["search_vector"]),
        ]
        ordering = ['id']  # Default ordering by ID in ascending order

    def __str__(self):
        return f"{self.chapter.title} - {self.title}"


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)
    search_vector = SearchVectorField(null=True, blank=True)  # For full-text search

    class Meta:
        indexes = [
            Index(fields=["search_vector"]),
        ]
        ordering = ['id']  # Default ordering by ID in ascending order

    def __str__(self):
        return self.category


class Topic(models.Model):
    # youtube_link = models.ManyToManyField('YouTubeLink', related_name='topics_links')  # Changed related_name to avoid conflict
    
    youtube_link = models.ForeignKey('YouTubeLink', related_name='topics', on_delete=models.CASCADE)  # Changed related_name to avoid conflict
    # video = models.ForeignKey(YouTubeVideo, related_name='timestamps', on_delete=models.CASCADE)
    topic_title = models.CharField(max_length=255)
    youtube_timestamp = models.CharField(max_length=8, null=True, blank=True)  # Optional YouTube timestamp
    # importent_topic = models.CharField(max_length=8, null=True, blank=True)  # Optional YouTube timestamp


    class Meta:
        ordering = ['topic_title']

    def __str__(self):
        return self.topic_title


class Question(models.Model):
    # youtube_link = models.ManyToManyField('YouTubeLink', related_name='questions_links')  # Changed related_name to avoid conflict
    youtube_link = models.ForeignKey('YouTubeLink', related_name='questions', on_delete=models.CASCADE)  # Changed related_name to avoid conflict
   
    question_text = models.TextField()
    youtube_timestamp = models.CharField(max_length=8, null=True, blank=True)  # Optional YouTube timestamp
    # importent_question = models.CharField(max_length=8, null=True, blank=True)  # Optional YouTube timestamp

    class Meta:
        ordering = ['question_text']

    def __str__(self):
        return self.question_text[:50]  # Return first 50 characters of the question


class YouTubeLink(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    subheadings = models.ManyToManyField(Subheading, related_name="youtube_links_subheading", blank=True)  # Many-to-Many with Subheading
    # topics = models.ManyToManyField(Topic, related_name="youtube_links_topic", blank=True)  # Many-to-Many with Topic
    # questions = models.ManyToManyField(Question, related_name="youtube_links_question", blank=True)  # Many-to-Many with Question
    categories = models.ManyToManyField(Category, related_name="youtube_links_categories", blank=True)  # Many-to-Many with Category

    def embed_url_id(self):
        """Extract the YouTube video ID from the URL."""
        if "v=" in self.url:
            return self.url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in self.url:
            return self.url.split("youtu.be/")[1]
        return None

    def __str__(self):
        return self.url
