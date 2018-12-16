

# Register your models here.
from django.contrib import admin

import movies.models as models


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
	fields = [
		'genre'
	]

	list_display = [
		'genre'
	]

	#list_filter = ['region', 'sub_region', 'intermediate_region', 'dev_status']
	##list_filter = ['dev_status']
# admin.site.register(models.CountryArea)


@admin.register(models.PlotKeyword)
class PlotKeywordAdmin(admin.ModelAdmin):
	fields = [
		'keyword'
	]

	list_display = [
		'keyword'
	]

@admin.register(models.Color)
class ColorAdmin(admin.ModelAdmin):
	fields = ['color_name']
	list_display = ['color_name']
	ordering = ['color_name']

# admin.site.register(models.DevStatus)

'''
@admin.register(models.HeritageSite)
class HeritageSiteAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields': (
				'site_name',
				'heritage_site_category',
				'description',
				'justification',
				'date_inscribed'
			)
		}),
		('Location and Area', {
			'fields': [
				(
					'longitude',
					'latitude'
				),
				'area_hectares',
				'transboundary'
			]
		})
	)

	list_display = (
		'site_name',
		'date_inscribed',
		'area_hectares',
		'heritage_site_category',
		'country_area_display'
	)

	list_filter = (
		'heritage_site_category',
		'date_inscribed'
	)

# admin.site.register(models.HeritageSite)
'''


@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):

	fields: [
		'movie_title',
		'title_year',
		'duration',
		'imdb_score',
		'movie_imdb_link',
		'color',
		'director',
		'language',
		'country_area',
		'content_rating',
		'genre',
		'keyword'
	]

	list_display = [
			'movie_title',
			'title_year',
			'duration',
			'imdb_score',
			'movie_imdb_link',
			'color',
			'director',
			'language',
			'country_area',
			'content_rating',
	]



# admin.site.register(models.HeritageSite)

@admin.register(models.ContentRating)
class ContentRatingAdmin(admin.ModelAdmin):
	fields = ['content_rating']
	list_display = ['content_rating']
	ordering = ['content_rating']

# admin.site.register(models.HeritageSiteCategory)


@admin.register(models.CountryArea)
class CountryAreaAdmin(admin.ModelAdmin):
	fields = [
		'country_area_name',
		#(
		#	'region',
		#	'sub_region',
		#	'intermediate_region'
		#),
		'iso_alpha3_code',
		'location',
		'm49_code',
		'dev_status'
	]

	list_display = [
		'country_area_name',
		#'region',
		#'sub_region',
		#'intermediate_region',
		'iso_alpha3_code',
		'm49_code',
		'dev_status'
	]

	#list_filter = ['region', 'sub_region', 'intermediate_region', 'dev_status']
	list_filter = ['dev_status']
# admin.site.register(models.CountryArea)


@admin.register(models.DevStatus)
class DevStatusAdmin(admin.ModelAdmin):
	fields = ['dev_status_name']
	list_display = ['dev_status_name']
	ordering = ['dev_status_name']

# admin.site.register(models.DevStatus)


@admin.register(models.Director)
class DirectorAdmin(admin.ModelAdmin):
	fields = ['director_name']
	list_display = ['director_name']
	ordering = ['director_name']

# admin.site.register(models.Region)


@admin.register(models.MovieLanguage)
class MovieLanguageAdmin(admin.ModelAdmin):
	fields = ['language_name']
	list_display = ['language_name']
	ordering = ['language_name']

# admin.site.register(models.SubRegion)

