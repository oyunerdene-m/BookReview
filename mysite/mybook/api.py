from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
import requests

from .models import Book, Review

def search(request):
    try:
      search = request.GET.get('search', None)
      if not search:
        raise KeyError
       
      found_result = Book.objects.filter(title__icontains=search) | Book.objects.filter(isbn__icontains=search) | Book.objects.filter(author__icontains=search)

      data = []
      for e in found_result:
        book = {'id': e.id, 'isbn': e.isbn, 'title': e.title, 'author': e.author, 'year': e.year}
        data.append(book)

      if len(data) == 0:
        return JsonResponse({"success": False})
    
    except KeyError:
      return render(request, "mybook/error.html", {"message": "buglu"})
    except Book.DoesNotExist:
      raise Http404("Book does not exist")
      # return render(request, "mybook/error.html", {"message": "No matched book."})
    
    response = JsonResponse({'books': data, 'success': True})
    response["Access-Control-Allow-Origin"] = "http://localhost:5500"
    return response

def get_book(request, book_id):
  found_book = Book.objects.get(pk=book_id)

  book = {'isbn': found_book.isbn, 'title': found_book.title, 'year': found_book.year, 'author': found_book.author}
  response = JsonResponse({"book": book})
  response["Access-Control-Allow-Origin"] = "http://localhost:5500"
  return response
    
def get_reviews(request, book_id):
    found_book = Book.objects.get(pk=book_id)
    reviews = found_book.reviews.all()
    data = []
    for e in reviews:
      r = {'content': e.content, 'createdAt': e.createdAt, 'rating': e.rating, 'username': e.user.username}
      data.append(r)
    response = JsonResponse({"reviews": data})
    response["Access-Control-Allow-Origin"] = "http://localhost:5500"
    return response
      
def add_review(request, book_id):
    try:
        user_id = 1 #request.user.id
        current_user = User.objects.get(pk=user_id)
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise Http404("Book does not exist.")
    # context = {
    #    "book": book
    #   }

    # if request.method == "GET":
    #     reviews = Review.objects.filter(user = current_user, book = book)
    #     review_count = len(reviews)
    #     if review_count > 0:
    #       return render(request, "mybook/error.html", {"message": "Sorry, you can add only one comment."})
        
    #     return render(request, "mybook/add_review.html", context)
    # else:
      #form validation!!!
    content = request.POST.get("content", None)
    rating = request.POST.get("rating", None)
    review = Review(content=content, rating=rating, user=current_user, book=book)
    review.save()
    book.reviews.add(review)

    review = {'content': review.content, 'rating': review.rating, 'createdAt': review.createdAt, 'username': review.user.username}
    response = JsonResponse({'review': review})
    response["Access-Control-Allow-Origin"] = "http://localhost:5500"
    return response
