from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^ajax/embeddings', views.ajax_get_embeddings, name='Ajax request for embeddings'),
	url(r'^ajax/genres', views.ajax_get_genres, name='Ajax request for genre list'),
    url(r'^ajax/movies', views.ajax_get_movies, name='Ajax request for movie list'),
    url(r'^ajax/top_neighbours', views.ajax_get_top_neighbours, name='Ajax request for top neighbours'),
    url(r'^movies/p1', views.top_k_neighbours, name='Top K neighbours'),
    url(r'^movies/p2', views.feature_visualization, name='Feature Visualization'),
    url(r'^', views.index, name='Index page'),
]