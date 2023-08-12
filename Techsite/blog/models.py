from django.db import models
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default= timezone.now)
    publish_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.publish_date = timezone.now
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comments=True) # type: ignore

    def get_absolute_url(self):
        return reverse('post.detail', kwargs={'pk': self.pk})

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=120)
    text = models.TextField()
    create_date = models.DateTimeField(default= timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self) -> str:
        return self.text
    
    def get_absolute_url(self):
        return reverse('post.list')
