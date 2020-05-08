from django.urls import path

from . import views
from . import api

urlpatterns = [
  path("", views.index, name="index"),
  path("book/<int:book_id>", views.more, name="more"),
  path("register", views.register, name="register"),
  path("login", views.login, name="login"),
  path("logout", views.logout, name="logout"),

  path("api/books/search", api.search, name="search"),
  path("api/book/reviews/<int:book_id>", api.get_reviews, name="get_reviews"),
  path("api/review/new/<int:book_id>", api.add_review, name="add_review"),
  path("api/book/<int:book_id>", api.get_book, name="get_book"),
  #///
  path("book/<int:book_id>/review/<int:review_id>/edit", views.edit_review, name="edit_review")
]