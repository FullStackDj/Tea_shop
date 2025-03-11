from django.db import models


class Page(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    text_on_page = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
