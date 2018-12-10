from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext

def index(request):
	return render(request, 'movies/index.html', {})

def page1(request):
	return render(request, 'movies/top_k_neighbours.html', {})

def page2(request):
	return render(request, 'movies/feature_visualization.html', {})