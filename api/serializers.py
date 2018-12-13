from movies.models import Movie, Director, Color, \
	Genre, PlotKeyword, MovieLanguage, Country, ContentRating, MovieGenres, MovieKeywords
from rest_framework import response, serializers, status

'''
class PlanetSerializer(serializers.ModelSerializer):

	class Meta:
		model = Planet
		fields = ('planet_id', 'planet_name', 'unsd_name')'''

class ColorSerializer(serializers.ModelSerializer):

	class Meta:
		model = Color
		fields = ('color_id', 'color_name')		
		
		

class ContentRatingSerializer(serializers.ModelSerializer):

	class Meta:
		model = ContentRating
		fields = ('content_rating_id', 'content_rating')


class CountrySerializer(serializers.ModelSerializer):

	class Meta:
		model = Country
		fields = ('country_id', 'country_name')


class DirectorSerializer(serializers.ModelSerializer):

	class Meta:
		model = Director
		fields = ('director_id', 'director_name')


class GenreSerializer(serializers.ModelSerializer):

	class Meta:
		model = Genre
		fields = ('genre_id', 'genre')		


class MovieLanguageSerializer(serializers.ModelSerializer):

	class Meta:
		model = MovieLanguage
		fields = ('language_id', 'language_name')	


class PlotKeywordSerializer(serializers.ModelSerializer):

	class Meta:
		model = PlotKeyword
		fields = ('keyword_id', 'keyword')


'''
class HeritageSiteJurisdictionSerializer(serializers.ModelSerializer):
	heritage_site_id = serializers.ReadOnlyField(source='heritage_site.heritage_site_id')
	country_area_id = serializers.ReadOnlyField(source='country_area.country_area_id')

	class Meta:
		model = HeritageSiteJurisdiction
		fields = ('heritage_site_id', 'country_area_id')
'''

class MovieGenresSerializer(serializers.ModelSerializer):
	movie_id = serializers.ReadOnlyField(source='movie.movie_id')
	genre_id = serializers.ReadOnlyField(source='genre.genre_id')

	class Meta:
		model = MovieGenres
		fields = ('movie_id', 'genre_id')
		
class MovieKeywordsSerializer(serializers.ModelSerializer):
	movie_id = serializers.ReadOnlyField(source='movie.movie_id')
	keyword_id = serializers.ReadOnlyField(source='keyword.keyword_id')

	class Meta:
		model = MovieKeywords
		fields = ('movie_id', 'keyword_id')		

		
'''		
class HeritageSiteSerializer(serializers.ModelSerializer):
	site_name = serializers.CharField(
		allow_blank=False,
		max_length=255
	)
	description = serializers.CharField(
		allow_blank=False
	)
	justification = serializers.CharField(
		allow_blank=True
	)
	date_inscribed = serializers.IntegerField(
		allow_null=True
	)
	longitude = serializers.DecimalField(
		allow_null=True,
		max_digits=11,
		decimal_places=8)
	latitude = serializers.DecimalField(
		allow_null=True,
		max_digits=10,
		decimal_places=8
	)
	area_hectares = serializers.FloatField(
		allow_null=True
	)
	transboundary = serializers.IntegerField(
		allow_null=False
	)
	heritage_site_category = HeritageSiteCategorySerializer(
		many=False,
		read_only=True
	)
	heritage_site_category_id = serializers.PrimaryKeyRelatedField(
		allow_null=False,
		many=False,
		write_only=True,
		queryset=HeritageSiteCategory.objects.all(),
		source='heritage_site_category'
	)
	heritage_site_jurisdiction = HeritageSiteJurisdictionSerializer(
		source='heritage_site_jurisdiction_set', # Note use of _set
		many=True,
		read_only=True
	)
	jurisdiction_ids = serializers.PrimaryKeyRelatedField(
		many=True,
		write_only=True,
		queryset=CountryArea.objects.all(),
		source='heritage_site_jurisdiction'
	)

	class Meta:
		model = HeritageSite
		fields = (
			'heritage_site_id',
			'site_name',
			'description',
			'justification',
			'date_inscribed',
			'longitude',
			'latitude',
			'area_hectares',
			'transboundary',
			'heritage_site_category',
			'heritage_site_category_id',
			'heritage_site_jurisdiction',
			'jurisdiction_ids'
		)

	def create(self, validated_data):
		"""
		This method persists a new HeritageSite instance as well as adds all related
		countries/areas to the heritage_site_jurisdiction table.  It does so by first
		removing (validated_data.pop('heritage_site_jurisdiction')) from the validated
		data before the new HeritageSite instance is saved to the database. It then loops
		over the heritage_site_jurisdiction array in order to extract each country_area_id
		element and add entries to junction/associative heritage_site_jurisdiction table.
		:param validated_data:
		:return: site
		"""

		# print(validated_data)

		countries = validated_data.pop('heritage_site_jurisdiction')
		site = HeritageSite.objects.create(**validated_data)

		if countries is not None:
			for country in countries:
				HeritageSiteJurisdiction.objects.create(
					heritage_site_id=site.heritage_site_id,
					country_area_id=country.country_area_id
				)
		return site

	def update(self, instance, validated_data):
		# site_id = validated_data.pop('heritage_site_id')
		site_id = instance.heritage_site_id
		new_countries = validated_data.pop('heritage_site_jurisdiction')

		instance.site_name = validated_data.get(
			'site_name',
			instance.site_name
		)
		instance.description = validated_data.get(
			'description',
			instance.description
		)
		instance.justification = validated_data.get(
			'justification',
			instance.justification
		)
		instance.date_inscribed = validated_data.get(
			'date_inscribed',
			instance.date_inscribed
		)
		instance.longitude = validated_data.get(
			'longitude',
			instance.longitude
		)
		instance.latitude = validated_data.get(
			'latitude',
			instance.latitude
		)
		instance.area_hectares = validated_data.get(
			'area_hectares',
			instance.area_hectares
		)
		instance.heritage_site_category_id = validated_data.get(
			'heritage_site_category_id',
			instance.heritage_site_category_id
		)
		instance.transboundary = validated_data.get(
			'transboundary',
			instance.transboundary
		)
		instance.save()

		# If any existing country/areas are not in updated list, delete them
		new_ids = []
		old_ids = HeritageSiteJurisdiction.objects \
			.values_list('country_area_id', flat=True) \
			.filter(heritage_site_id__exact=site_id)

		# TODO Insert may not be required (Just return instance)

		# Insert new unmatched country entries
		for country in new_countries:
			new_id = country.country_area_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				HeritageSiteJurisdiction.objects \
					.create(heritage_site_id=site_id, country_area_id=new_id)

		# Delete old unmatched country entries
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				HeritageSiteJurisdiction.objects \
					.filter(heritage_site_id=site_id, country_area_id=old_id) \
					.delete()

		return instance
'''	
class MovieSerializer(serializers.ModelSerializer):
	movie_title = serializers.CharField(
		allow_blank=False,
		max_length=255
	)
	movie_imdb_link = serializers.CharField(
		allow_blank=False
	)
	title_year = serializers.IntegerField(
		allow_null=False
	)
	imdb_score = serializers.DecimalField(
		allow_null=False,
		max_digits=2,
		decimal_places=1)
		
	duration = serializers.IntegerField(
		allow_null=False
	)
	
	color = ColorSerializer(
		many=False,
		read_only=True
	)
	color_id = serializers.PrimaryKeyRelatedField(
		allow_null=False,
		many=False,
		write_only=True,
		queryset=Color.objects.all(),
		source='color'
	)

	content_rating = ContentRatingSerializer(
		many=False,
		read_only=True
	)
	content_rating_id = serializers.PrimaryKeyRelatedField(
		allow_null=False,
		many=False,
		write_only=True,
		queryset=ContentRating.objects.all(),
		source='content_rating'
	)

	country = CountrySerializer(
		many=False,
		read_only=True
	)
	country_id = serializers.PrimaryKeyRelatedField(
		allow_null=False,
		many=False,
		write_only=True,
		queryset=Country.objects.all(),
		source='country'
	)	

	director = DirectorSerializer(
		many=False,
		read_only=True
	)
	director_id = serializers.PrimaryKeyRelatedField(
		allow_null=False,
		many=False,
		write_only=True,
		queryset=Director.objects.all(),
		source='director'
	)	


	language = MovieLanguageSerializer(
		many=False,
		read_only=True
	)
	language_id = serializers.PrimaryKeyRelatedField(
		allow_null=False,
		many=False,
		write_only=True,
		queryset=MovieLanguage.objects.all(),
		source='movie_language'
	)	
	
	movie_genres = MovieGenresSerializer(
		source='movie_genres_set', # Note use of _set
		many=True,
		read_only=True
	)
	movie_genres_ids = serializers.PrimaryKeyRelatedField(
		many=True,
		write_only=True,
		queryset=Genre.objects.all(),
		source='movie_genres'
	)
	
	movie_keywords = MovieKeywordsSerializer(
		source='movie_keywords_set', # Note use of _set
		many=True,
		read_only=True
	)
	movie_keywords_ids = serializers.PrimaryKeyRelatedField(
		many=True,
		write_only=True,
		queryset=PlotKeyword.objects.all(),
		source='movie_keywords'
	)	

	class Meta:
		model = Movie
		fields = (
			'movie_id',
			'movie_title',
			'movie_imdb_link',
			'title_year',
			'imdb_score',
			'duration',
			'color',
			'color_id',
			'content_rating',
			'content_rating_id',
			'country',
			'country_id',
			'director',
			'director_id',
			'language',
			'language_id',
			'movie_genres',
			'movie_genres_ids',
			'movie_keywords',
			'movie_keywords_ids',
		)

	def create(self, validated_data):
		"""
		This method persists a new HeritageSite instance as well as adds all related
		countries/areas to the heritage_site_jurisdiction table.  It does so by first
		removing (validated_data.pop('heritage_site_jurisdiction')) from the validated
		data before the new HeritageSite instance is saved to the database. It then loops
		over the heritage_site_jurisdiction array in order to extract each country_area_id
		element and add entries to junction/associative heritage_site_jurisdiction table.
		:param validated_data:
		:return: site
		"""

		# print(validated_data)

		genres = validated_data.pop('movie_genres')
		movie = Movie.objects.create(**validated_data)

		if genres is not None:
			for genre in genres:
				MovieGenres.objects.create(
					movie_id=movie.movie_id,
					genre_id=genre.genre_id
				)
		keywords = validated_data.pop('movie_keywords')
		movie = Movie.objects.create(**validated_data)

		if keywords is not None:
			for keyword in keywords:
				MovieKeywords.objects.create(
					movie_id=movie.movie_id,
					keyword_id=keyword.keyword_id
				)				
		return movie

		
	def update(self, instance, validated_data):
		# site_id = validated_data.pop('heritage_site_id')
		movie_id = instance.movie_id
		new_genres = validated_data.pop('movie_genres')
		new_keywords = validated_data.pop('movie_keywords')
		
		instance.movie_title = validated_data.get(
			'movie_title',
			instance.movie_title
		)
		instance.movie_imdb_link = validated_data.get(
			'movie_imdb_link',
			instance.movie_imdb_link
		)
		instance.title_year = validated_data.get(
			'title_year',
			instance.title_year
		)
		instance.imdb_score = validated_data.get(
			'imdb_score',
			instance.imdb_score
		)
		instance.duration = validated_data.get(
			'duration',
			instance.duration
		)
		instance.color_id = validated_data.get(
			'color_id',
			instance.color_id
		)
		instance.content_rating_id = validated_data.get(
			'content_rating_id',
			instance.content_rating_id
		)		
		instance.country_id = validated_data.get(
			'country_id',
			instance.country_id
		)		
		instance.director_id = validated_data.get(
			'director_id',
			instance.director_id
		)		
		instance.language_id = validated_data.get(
			'language_id',
			instance.language_id
		)
		instance.save()

		# If any existing country/areas are not in updated list, delete them
		new_ids = []
		old_ids = MovieGenres.objects \
			.values_list('genre_id', flat=True) \
			.filter(movie_id__exact=movie_id)

		# TODO Insert may not be required (Just return instance)

		# Insert new unmatched country entries
		for genre in new_genres:
			new_id = genre.genre_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				MovieGenres.objects \
					.create(movie_id=movie_id, genre_id=new_id)

		# Delete old unmatched country entries
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				MovieGenres.objects \
					.filter(movie_id=movie_id, genre_id=old_id) \
					.delete()

		new_ids = []
		old_ids = MovieKeywords.objects \
			.values_list('keyword_id', flat=True) \
			.filter(movie_id__exact=movie_id)

		# TODO Insert may not be required (Just return instance)

		# Insert new unmatched country entries
		for keyword in new_keywords:
			new_id = keyword.keyword_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				MovieKeywords.objects \
					.create(movie_id=movie_id, keyword_id=new_id)

		# Delete old unmatched country entries
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				MovieKeywords.objects \
					.filter(movie_id=movie_id, keyword_id=old_id) \
					.delete()					

		return instance	