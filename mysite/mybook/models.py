from django.db import models
import datetime
from django.utils.timezone import utc

# Create your models here.
class User(models.Model):
  username = models.CharField(max_length=60)
  password = models.CharField(max_length=128)

  def __str__(self):
    return f"{self.id}: {self.username}"


class Book(models.Model):
  isbn = models.CharField(max_length=128)
  title = models.CharField(max_length=60)
  author = models.CharField(max_length=60)
  year = models.CharField(max_length=60)

  def __str__(self):
    return f"isbn-{self.isbn}, {self.title}, by {self.author}, in {self.year}."

  
class Review(models.Model):
  content = models.TextField(default='')
  createdAt = models.DateTimeField(default=datetime.datetime(2015, 7, 20, 15, 30, 4, 971732, tzinfo=utc))
  rating = models.IntegerField(blank=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  book = models.ForeignKey(Book, on_delete=models.CASCADE)
  def __str__(self):
    return f"{self.content}, rating:{self.rating} createdAt:{self.createdAt}"
  
# to see sql command by migrate code: mysite oonoo$ python manage.py sqlmigrate mybook 0001
