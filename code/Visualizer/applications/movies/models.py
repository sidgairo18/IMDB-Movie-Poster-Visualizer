from django.db import models

class Genre(models.Model):
	name = models.CharField(max_length=200)

	def serialize(cls):
		return {
			'id': cls.id,
			'name': cls.name,
		}

class Movie(models.Model):
	name = models.CharField(max_length=200)
	genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
	year = models.IntegerField(default=2018)

	def serialize(cls):
		return {
			'id': cls.id,
			'genre_id': cls.genre_id,
			'name': cls.name,
			'year': cls.year,
		}