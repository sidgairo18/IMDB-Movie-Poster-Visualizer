from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from applications.movies.models import *
import applications.utils as utils 
import visualizer.settings as settings
import json
import os

def index(request):
	return render(request, 'movies/index.html', {})

def top_k_neighbours(request):
	return render(request, 'movies/top_k_neighbours.html', {})

def feature_visualization(request):
	return render(request, 'movies/embeddings.html', {})

def ajax_get_embeddings(request):
	syear = None
	eyear = None
	categories = None
	andopr = None
	feature = None
	if 'syear' in request.GET:
		syear = request.GET['syear']
	if 'eyear' in request.GET:
		eyear = request.GET['eyear']
	if 'category[]' in request.GET:
		categories = request.GET.getlist('category[]')
	if 'andopr' in request.GET:
		andopr = request.GET['andopr']
		andopr = True if (andopr == 'true') else False
	if 'feature' in request.GET:
		feature = request.GET['feature']

	movies = get_movies_range(syear=syear, eyear=eyear, categories=categories, andopr=andopr)
	if len(movies) > 0:
		# X_t, Y_t, I_t = utils.preprocess_data(settings.FEATURES[feature], settings.DATASET, movies)
		# plot = utils.visualize_features(X_t, Y_t, I_t, min(settings.E_PCA, X_t.shape[0]))
		X_cor, Y_cor, I_t = utils.get_plot_values(settings.DATASET, movies, feature)
		plot = utils.bokeh_plot(I_t, X_cor, Y_cor)
		print('got plot from the list')
	else:
		return HttpResponse(json.dumps({
				'error': 'No movies in this category'
			}), content_type="application/json", status=200)
	return HttpResponse(json.dumps({
			'plot': plot
		}), content_type="application/json", status=200)

def ajax_get_movies(request):
	syear = None
	eyear = None
	categories = None
	andopr = None
	if 'syear' in request.GET:
		syear = request.GET['syear']
	if 'eyear' in request.GET:
		eyear = request.GET['eyear']
	if 'category[]' in request.GET:
		categories = request.GET.getlist('category[]')
	if 'andopr' in request.GET:
		andopr = request.GET['andopr']
		andopr = True if (andopr == 'true') else False

	movies = get_movies_range(syear=syear, eyear=eyear, categories=categories, andopr=andopr)
	return HttpResponse(json.dumps({
			'total': len(movies),
			'movies': movies
		}), content_type="application/json", status=200)

def ajax_get_genres(request):
	genres = get_genres()
	return HttpResponse(json.dumps({
			'total': len(genres),
			'genres': genres
		}), content_type="application/json", status=200)

def ajax_get_features(request):
	features = get_features()
	return HttpResponse(json.dumps({
			'total': len(features),
			'features': features
		}), content_type="application/json", status=200)

def ajax_get_top_neighbours(request):
	image = None
	k = None
	feature = None
	if 'image' in request.GET:
		image = request.GET['image']
	if 'k' in request.GET:
		k = int(request.GET['k'])
	if 'feature' in request.GET:
		feature = request.GET['feature']
	if feature not in settings.FEATURES:
		raise Exception('path for this feature not specified')

	movies = get_movies()
	movies = utils.get_top_neighbours(settings.FEATURES[feature], image, movies, k)
	for movie in movies:
		movie['genres'] = get_genres_by_movie(movie)
	return HttpResponse(json.dumps({
			'total': len(movies),
			'movies': movies
		}), content_type="application/json", status=200)

def get_genres_by_movie(movie):
	movie = Movie.objects.filter(id=movie['id']).first()
	items = MovieToGenre.objects.filter(movie=movie)
	genres = []
	for item in items:
		genres.append(item.genre.serialize()['name'])
	return genres

def get_movies(year=None, category=None):
	items = MovieToGenre.objects.select_related('movie', 'genre')
	if year != None:
		items = items.filter(movie__year=year)
	if category != None:
		items = items.filter(genre__name=category)
	movies = [item.movie.serialize() for item in items]
	movies = utils.filter_unique(movies, 'image')
	return movies

def get_genres():
	items = Genre.objects.all()
	genres = [item.serialize() for item in items]
	return genres

def get_features():
	items = Feature.objects.all()
	features = [item.serialize() for item in items]
	return features

def get_movies_range(syear, eyear, categories, andopr):
	items = MovieToGenre.objects.select_related('movie', 'genre')
	if syear != None:
		items = items.filter(movie__year__gte=syear)
	if eyear != None:
		items = items.filter(movie__year__lte=eyear)
	if categories != None and andopr != None:
		if andopr == True:
			movies = set(items.values_list('movie', flat=True))
			for category in categories:
				movies = movies.intersection(set(items.filter(genre__name=category).values_list('movie', flat=True)))
			movies = list(movies)
			if len(movies) > 0:
				queries = [Q(id=movie_id) for movie_id in movies]
				query = queries.pop()
				for item in queries:
					query |= item
				items = Movie.objects.filter(query)
				movies = [item.serialize() for item in items]
				return movies
			return []
		else:
			queries = [Q(genre__name=category) for category in categories]
			query = queries.pop()
			for item in queries:
				query |= item
			items = items.filter(query)
	movies = [item.movie.serialize() for item in items]
	movies = utils.filter_unique(movies, 'image')
	return movies