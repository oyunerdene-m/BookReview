from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
class Book(models.Model):
  isbn = models.CharField(max_length=128)
  title = models.CharField(max_length=60)
  author = models.CharField(max_length=60)
  year = models.CharField(max_length=60)

  def __str__(self):
    return f"isbn-{self.isbn}, {self.title}, by {self.author}, in {self.year}."

  
class Review(models.Model):
  content = models.TextField(default='')
  createdAt = models.DateTimeField(auto_now_add=True)
  rating = models.IntegerField(blank=True)
  book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
  def __str__(self):
    return f"{self.content}, rating:{self.rating} createdAt:{self.createdAt}"
  
# to see sql command by migrate code: mysite oonoo$ python manage.py sqlmigrate mybook 0001
