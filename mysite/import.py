import os
import csv


from mybook.models import Book

with open('books.csv') as f:
  reader = csv.DictReader(f)
  for row in reader:
      b = Book(isbn=row['isbn'], title=row['title'], author=row['author'], year=row['year'])
      b.save()