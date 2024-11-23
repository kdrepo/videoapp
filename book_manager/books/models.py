from django.db import models


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

    def __str__(self):
        return f"{self.book.title} - {self.title}"


class Subheading(models.Model):
    chapter = models.ForeignKey(Chapter, related_name="subheadings", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField()
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.chapter.title} - {self.title}"


class Subheading2(models.Model):
    subheading = models.ForeignKey(Subheading, related_name="subheadings2", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField()
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.subheading.title} - {self.title}"


class YouTubeLink(models.Model):
    url = models.URLField()
    description = models.CharField(max_length=255, blank=True, null=True)
    chapter = models.ForeignKey(Chapter, related_name="youtube_links", on_delete=models.CASCADE, blank=True, null=True)
    subheading = models.ForeignKey(Subheading, related_name="youtube_links", on_delete=models.CASCADE, blank=True, null=True)
    subheading2 = models.ForeignKey(Subheading2, related_name="youtube_links", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.url
