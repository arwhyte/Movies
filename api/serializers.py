from movies.models import Movie, Director, Color, \
	Genre, PlotKeyword, MovieLanguage, CountryArea, ContentRating, MovieGenres, MovieKeywords, DevStatus
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

class DevStatusSerializer(serializers.ModelSerializer):

	class Meta:
		model = DevStatus
		fields = ('dev_status_id', 'dev_status_name')
		
class CountryAreaSerializer(serializers.ModelSerializer):
	dev_status = DevStatusSerializer(many=False, read_only=True)

	class Meta:
		model = CountryArea
		fields = ('country_area_id', 'country_area_name','m49_code','iso_alpha3_code','dev_status',)


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


		
#find source in Module Movie table
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

	country_area = CountryAreaSerializer(
		many=False,
		read_only=True
	)

	country_id = serializers.PrimaryKeyRelatedField(
		allow_null=False,
		many=False,
		write_only=True,
		queryset=CountryArea.objects.all(),
		source='country_area'
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
		source='language'#find source in Module Movie table
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
		source='genre'
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
		source='keyword'
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
			'country_id',
			'country_area',
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

		#print(validated_data)

		genres = validated_data.pop('genre')
		keywords = validated_data.pop('keyword')
		movie = Movie.objects.create(**validated_data)

		if genres is not None:
			for genre in genres:
				MovieGenres.objects.create(
					movie_id=movie.movie_id,
					genre_id=genre.genre_id
				)

		if keywords is not None:
			for keyword in keywords:
				MovieKeywords.objects.create(
					movie_id=movie.movie_id,
					keyword_id=keyword.keyword_id
				)
		return movie
	'''
	for keyword in keywords:
		instance = MovieKeywords.objects.create(
			movie_id=movie.movie_id
		)
		keys = MovieKeywords.objects.filter(keyword_id=keyword.keyword_id)
		instance.keyword_id.set(keys)
	'''


	def update(self, instance, validated_data):
		print(validated_data)
		movie_id = instance.movie_id
		new_genres = validated_data.pop('genre')
		new_keywords = validated_data.pop('keyword')
		#new_country = validated_data.get('country_area')
		#print(new_country)
	
		
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
		instance.color = validated_data.get(
			'color',
			instance.color
		)
		instance.content_rating = validated_data.get(
			'content_rating',
			instance.content_rating
		)
		instance.country_area = validated_data.get(
			'country_area',
			instance.country_area
		)
		instance.director = validated_data.get(
			'director',
			instance.director
		)
		instance.language = validated_data.get(
			'language',
			instance.language
		)
		instance.save()
		#for country in new_country:

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
