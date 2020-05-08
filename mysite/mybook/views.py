from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
import requests

from .models import Book, Review

# Create your views here.
def register(request):
  if request.method == 'GET':
    return render(request, "mybook/register.html")
  elif request.method == 'POST':
    try:
      username = request.POST["username"]
      password = request.POST["password"]
    except KeyError:
      return render(request, "mybook/error.html", {"message": "No selection."})
    # check if username exists in database!!
    user = User.objects.create_user(username, 'example@thebeatles.com', password)
    user.save()
    return HttpResponseRedirect(reverse("login"))
    #return render(request, "mybook/login.html", {"message": "Signed up."})

def login(request):
  if request.method == 'GET':
    if not request.user.is_authenticated:
      return render(request, "mybook/login.html")

    context = {
          "user": request.user
      }
      
    return render(request, "mybook/index.html", context)

  elif request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
      auth_login(request, user)
      return HttpResponseRedirect(reverse("index"))
    else:
      return render(request, "mybook/login.html", {"message": "Invalid credentials."})

def logout(request):
  auth_logout(request)
  return render(request, "mybook/login.html", {"message": "Logged out."})


#////////////////////////////////////////////////////
#app routes
def index(request):
  return render(request, "mybook/index.html")


def more(request, book_id):
    #form validation!!!
    try:
      found_book = Book.objects.get(pk=book_id)
      reviews = found_book.reviews.all()

    except Book.DoesNotExist:
      raise Http404("Book does not exist.")

    # isbn = found_book.isbn
    # res =  requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "aSHhhnXKPm2y1aV2Uhb8Q", "isbns": isbn})
    # result = res.json()
    # api_book_info = result['books'][0]
   
    api_book_info = {
        'work_ratings_count': 5,
        'average_rating': 4.0
    }
    context = {
      "book": found_book,
      "api_book_info": api_book_info,
      "reviews": reviews,
      "username": request.user,
    }
    return render(request, "mybook/more.html", context)


#/////
def edit_review(request, review_id, book_id):
  try:
    found_review = Review.objects.get(pk=review_id)
    found_book = Book.objects.get(pk=book_id)
  except KeyError:
    return render(request, "mybook/error.html", {"message": "Not Found."})
  except Review.DoesNotExist:
    raise Http404("Review does not exist.")
  except Book.DoesNotExist:
    raise Http404("Book does not exist.")
  
  #chosed_rating = found_review.rating
  #only show other ratings
  context = {
    "review": found_review,
    "book": found_book,
  }

  if request.method == "GET":
    return render(request, "mybook/edit_review.html", context)
  else:
    content = request.POST["content"]
    rating = request.POST["rating"]
    found_review.content = content
    found_review.rating = rating
    found_review.save()

    return HttpResponseRedirect(reverse("more", args=(book_id,)))
    




      




