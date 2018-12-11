from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('movies/', views.MovieListView.as_view(), name='movielist'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='singlemovie'),
    path('genres/', views.GenreListView.as_view(), name='genres'),
    path('genres/<int:pk>/', views.GenreDetailView.as_view(), name='genre_detail'),
	path('movies/new/', views.MovieCreateView.as_view(), name='movie_new')
]