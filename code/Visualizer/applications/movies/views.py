from django.http import HttpResponse
from django.shortcuts import render
from applications.movies.models import *
import applications.utils as utils 
import json

def index(request):
	return render(request, 'movies/index.html', {})

def top_k_neighbours(request):
	return render(request, 'movies/top_k_neighbours.html', {})

def feature_visualization(request):
	return render(request, 'movies/feature_visualization.html', {})

def ajax_get_movies(request):
	year = None
	category = None
	if 'year' in request.GET:
		year = request.GET['year']
	if 'category' in request.GET:
		category = request.GET['category']

	movies = get_movies(year=year, category=category)
	return HttpResponse(json.dumps({
			'total': len(movies),
			'movies': movies
		}), content_type="application/json", status=200)

def get_movies(year=None, category=None):
	items = MovieToGenre.objects.select_related('movie', 'genre')
	if year != None:
		items = items.filter(movie__year=year)
	if category != None:
		items = items.filter(genre__name=category)
	movies = [item.movie.serialize() for item in items]
	movies = utils.filter_unique(movies, 'image')
	return movies