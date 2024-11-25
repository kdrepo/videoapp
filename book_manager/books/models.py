from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.db.models import Index


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Chapter(models.Model):
    book = models.ForeignKey(Book, related_name="chapters", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField()
    text = models.TextField(blank=True, null=True)
    search_vector = SearchVectorField(null=True, blank=True)  # For full-text search

    class Meta:
        indexes = [
            Index(fields=["search_vector"]),
        ]

    def __str__(self):
        return f"{self.book.title} - {self.title}"


class Subheading(models.Model):
    chapter = models.ForeignKey(Chapter, related_name="subheadings", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField()
    text = models.TextField(blank=True, null=True)
    search_vector = SearchVectorField(null=True, blank=True)  # For full-text search

    class Meta:
        indexes = [
            Index(fields=["search_vector"]),
        ]

    def __str__(self):
        return f"{self.chapter.title} - {self.title}"


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)
    search_vector = SearchVectorField(null=True, blank=True)  # For full-text search

    class Meta:
        indexes = [
            Index(fields=["search_vector"]),
        ]

    def __str__(self):
        return self.category


class Topic(models.Model):
    topic = models.CharField(max_length=255)
    youtube_timestamp = models.CharField(max_length=8, null=True, blank=True)  # Optional YouTube timestamp
    search_vector = SearchVectorField(null=True, blank=True)  # For full-text search

    class Meta:
        indexes = [
            Index(fields=["search_vector"]),
        ]

    def __str__(self):
        return self.topic


class Question(models.Model):
    question_text = models.TextField()
    search_vector = SearchVectorField(null=True, blank=True)  # For full-text search

    class Meta:
        indexes = [
            Index(fields=["search_vector"]),
        ]

    def __str__(self):
        return self.question_text[:50]  # Return first 50 characters of the question


class YouTubeLink(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name="youtube_links", blank=True)  # Many-to-Many with Category
    topics = models.ManyToManyField(Topic, related_name="youtube_links", blank=True)  # Many-to-Many with Topic
    questions = models.ManyToManyField(Question, related_name="youtube_links", blank=True)  # Many-to-Many with Question
    chapter = models.ForeignKey(Chapter, related_name="youtube_links", on_delete=models.CASCADE, blank=True, null=True)  # Retained Chapter relationship
    subheading = models.ForeignKey(Subheading, related_name="youtube_links", on_delete=models.CASCADE, blank=True, null=True)  # Retained Subheading relationship

    def embed_url_id(self):
        # Extract the YouTube video ID from the URL
        if "v=" in self.url:
            return self.url.split("v=")[1].split("&")[0]
            # print(self.youtube_url.split("v=")[1].split("&")[0])
        elif "youtu.be/" in self.url:
            return self.url.split("youtu.be/")[1]
        return None
    
    def __str__(self):
        return self.url
