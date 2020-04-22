from django.urls import path

from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("search", views.search, name="search"),
  path("more/<int:book_id>", views.more, name="more"),
  path("review/new/<int:book_id>", views.add_review, name="add_review"),
  path("register", views.register, name="register"),
  path("login", views.login, name="login"),
  path("logout", views.logout, name="logout")
]