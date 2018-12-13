from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

from .models import Movie
from .models import Genre
from .models import MovieGenres
from .models import MovieKeywords

from .forms import MovieForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.shortcuts import redirect

from django_filters.views import FilterView
from .filters import MovieFilter



def index(request):
	return HttpResponse("Hello, world. You're at the UNESCO Heritage Sites index page.")


class AboutPageView(generic.TemplateView):
	template_name = 'movies/about.html'


class HomePageView(generic.TemplateView):
	template_name = 'movies/home.html'


class MovieListView(generic.ListView):
	model = Movie
	context_object_name = 'movies'
	template_name = 'movies/movie_list.html'
	paginate_by = 120

	def get_queryset(self):
		return Movie.objects.all()

class MovieDetailView(generic.DetailView):
	model = Movie
	context_object_name = 'moviedetail'
	template_name = 'movies/moviedetail.html'
	# TODO add the correct template string value
	
	
@method_decorator(login_required, name='dispatch')	
class GenreListView(generic.ListView):
	model = Genre
	context_object_name = 'genres'
	template_name = 'movies/genre_list.html'
	paginate_by = 20

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)	
	
	def get_queryset(self):
		return Genre.objects.all()

		
@method_decorator(login_required, name='dispatch')		
class GenreDetailView(generic.DetailView):
	model = Genre
	context_object_name = 'genredetail'
	template_name = 'movies/genredetail.html'	
	
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)	

		
@method_decorator(login_required, name='dispatch')
class MovieCreateView(generic.View):
	model = Movie
	form_class = MovieForm
	success_message = "Movie created successfully"
	template_name = 'movies/movie_new.html'
	# fields = '__all__' <-- superseded by form_class
	# success_url = reverse_lazy('heritagesites/site_list')

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):	
		form = MovieForm(request.POST)
		if form.is_valid():	
			new_movie = form.save(commit=False)
			new_movie.save()
			print(form.cleaned_data)
			for new_keyword in form.cleaned_data['keyword'].all():
				print(new_keyword)		
				MovieKeywords.objects.create(movie=new_movie, keyword=new_keyword)				
			for new_genre in form.cleaned_data['genre']:
				print(new_genre)
				MovieGenres.objects.create(movie=new_movie, genre=new_genre)
				
			return redirect(new_movie) # shortcut to object's get_absolute_url()
			# return HttpResponseRedirect(site.get_absolute_url())
		return render(request, 'movies/movie_new.html', {'form': form})

	def get(self, request):
		form = MovieForm()
		return render(request, 'movies/movie_new.html', {'form': form})	

		
@method_decorator(login_required, name='dispatch')
class MovieUpdateView(generic.UpdateView):
	model = Movie
	form_class = MovieForm
	# fields = '__all__' <-- superseded by form_class
	context_object_name = 'moviedetail'
	# pk_url_kwarg = 'site_pk'
	success_message = "Movie updated successfully"
	template_name = 'movies/movie_update.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def form_valid(self, form):
		movie = form.save(commit=False)
		# site.updated_by = self.request.user
		# site.date_updated = timezone.now()
		movie.save()

		# Current country_area_id values linked to site
		old_ids = MovieGenres.objects\
			.values_list('genre_id', flat=True)\
			.filter(movie_id=movie.movie_id)

		# New countries list
		new_genres = form.cleaned_data['genre']
		# New ids
		new_ids = []

		# Insert new unmatched country entries
		for genre in new_genres:
			new_id = genre.genre_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				MovieGenres.objects \
					.create(movie=movie, genre=genre)

		# Delete old unmatched country entries
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:			
				MovieGenres.objects \
					.filter(movie_id=movie.movie_id, genre_id=old_id) \
					.delete()
#keywords
		old_ids = MovieKeywords.objects\
			.values_list('keyword_id', flat=True)\
			.filter(movie_id=movie.movie_id)

		# New keywords list
		new_keywords = form.cleaned_data['keyword']
		# New ids
		new_ids = []

		# Insert new unmatched keyword entries
		for keyword in new_keywords:
			new_id = keyword.keyword_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				#print(keyword)				
				MovieKeywords.objects \
					.create(movie=movie, keyword=keyword)#keyword is the column of table MovieKeywords

		# Delete old unmatched country entries
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				MovieKeywords.objects \
					.filter(movie_id=movie.movie_id, keyword_id=old_id) \
					.delete()					

		return HttpResponseRedirect(movie.get_absolute_url())
		#return redirect('heritagesites/sites/', pk=site.pk)		
		
		
@method_decorator(login_required, name='dispatch')
class MovieDeleteView(generic.DeleteView):
	model = Movie
	success_message = "Movie deleted successfully"
	success_url = reverse_lazy('movielist')
	context_object_name = 'moviedetail'
	template_name = 'movies/movie_delete.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()

		# Delete movie&genre, movie&keywords entries
		MovieGenres.objects \
			.filter(movie_id=self.object.movie_id) \
			.delete()
		MovieKeywords.objects \
			.filter(movie_id=self.object.movie_id) \
			.delete()			

		self.object.delete()

		return HttpResponseRedirect(self.get_success_url())		

class MovieFilterView(FilterView):
	filterset_class = MovieFilter
	template_name = 'movies/movie_filter.html'		