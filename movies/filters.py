import django_filters
from movies.models import Movie, Director, Color, \
	Genre, PlotKeyword, MovieLanguage, CountryArea, ContentRating


class MovieFilter(django_filters.FilterSet):
	movie_name = django_filters.CharFilter(
		field_name='movie_title',
		label='Movie Name',
		lookup_expr='icontains'
	)

	year = django_filters.NumberFilter(
		field_name='title_year',
		label='Year',
		lookup_expr='icontains'
	)	

	director = django_filters.ModelChoiceFilter(
		field_name='director',
		label='Director',
		queryset=Director.objects.all().order_by('director_name'),
		lookup_expr='exact'
	)

	color = django_filters.ModelChoiceFilter(
		field_name='color',
		label='Color',
		queryset=Color.objects.all().order_by('color_name'),
		lookup_expr='exact'
	)	

	genre = django_filters.ModelChoiceFilter(
		field_name='genre',
		label='Genre',
		queryset=Genre.objects.all().order_by('genre'),
		lookup_expr='exact'
	)
	
	keyword = django_filters.ModelChoiceFilter(
		field_name='keyword',
		label='Keyword',
		queryset=PlotKeyword.objects.all().order_by('keyword'),
		lookup_expr='exact'
	)	
	
	language = django_filters.ModelChoiceFilter(
		field_name='language',
		label='Lauguage',
		queryset=MovieLanguage.objects.all().order_by('language_name'),
		lookup_expr='exact'
	)

	country_area = django_filters.ModelChoiceFilter(
		field_name='country_area',
		label='Country',
		queryset=CountryArea.objects.all().order_by('country_area_name'),
		lookup_expr='exact'
	)
	content_rating = django_filters.ModelChoiceFilter(
		field_name='content_rating',
		label='Content Rating',
		queryset=ContentRating.objects.all().order_by('content_rating'),
		lookup_expr='exact'
	)

	imdb_score = django_filters.CharFilter(
		field_name='imdb_score',
		label='Imdb_score',
		lookup_expr='icontains'
	)

	duration = django_filters.CharFilter(
		field_name='duration',
		label='Duration',
		lookup_expr='icontains'
	)
		


	class Meta:
		model = Movie
		# form = SearchForm
		# fields [] is required, even if empty.
		fields = []
