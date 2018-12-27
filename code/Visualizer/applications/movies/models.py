from django.db import models

class Genre(models.Model):
	name = models.CharField(max_length=200, null=True)

	def serialize(cls):
		return {
			'id': cls.id,
			'name': cls.name
		}

class Movie(models.Model):
	title = models.CharField(max_length=200, null=True)
	image = models.CharField(max_length=200, null=True)
	year = models.IntegerField(default=2018, null=True)
	country = models.CharField(max_length=200, null=True)
	director = models.CharField(max_length=200, null=True)
	plot = models.CharField(max_length=2000, null=True)
	rating = models.FloatField(default=10.0, null=True)

	def serialize(cls):
		return {
			'id': cls.id,
			'title': cls.title,
			'image': cls.image,
			'year': cls.year,
			'country': cls.country,
			'director': cls.director,
			'plot': cls.plot,
			'rating': cls.rating
		}

class MovieToGenre(models.Model):
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

	def serialize(cls):
		return {
			'movie': cls.movie.serialize(),
			'genre': cls.genre.serialize()
		}

class Feature(models.Model):
	name = models.CharField(max_length=200, null=True)
	desc = models.CharField(max_length=2000, null=True)

	def serialize(cls):
		return {
			'name': cls.name,
			'desc': cls.desc
		}

class FeatureToMovie(models.Model):
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
	feature = models.ForeignKey(Feature, on_delete=models.CASCADE, null=True)
	x = models.FloatField(default=0.0, null=True)
	y = models.FloatField(default=0.0, null=True)

	def serialize(cls):
		return {
			'movie': cls.movie.serialize(),
			'feature': cls.feature.serialize(),
			'x': cls.x,
			'y': cls.y
		}