from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    pass

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)

    def name(self):
        return f"{self.title}"
    def __str__(self):
        return f"{self.id}: {self.title}"

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="creator")
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    img = models.CharField(max_length=2048, blank=True)
    like = models.ManyToManyField("User", blank=True, related_name="like")
    enrolled = models.ManyToManyField("User", blank=True, related_name="enrolled")
    date = models.DateTimeField(default=timezone.now)

    def likes(self):
        return self.like.all().count()
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "img": self.img,
            "likes": self.likes(),
            "date": self.date.strftime("%b %d %y, %I:%M %p")
        }

class Unit(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course")
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    notes = models.CharField(max_length=2048)
    video = models.CharField(max_length=1024)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentor")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="commented")
    content = models.CharField(max_length=255)

