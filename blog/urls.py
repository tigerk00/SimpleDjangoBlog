from django.urls import path
from .views import *


urlpatterns = [
    path("",Home.as_view(),name="home"),
    path("category/<str:slug>/", PostsByCategory.as_view(), name="category"),
    path("tag/<str:slug>/", PostsByTag.as_view(), name="tag"),
    path("post/<str:slug>/", GetPost.as_view(), name="post"),
    path("search/", Search.as_view(), name="search"),
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout", user_logout,name="logout"),

    path("profile", user, name="profile"),

]