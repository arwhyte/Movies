from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

from .models import Movie
from .models import Genre
from .models import MovieGenres

from .forms import MovieForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.shortcuts import redirect

#from django_filters.views import FilterView
#from .filters import HeritageSiteFilter



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
	paginate_by = 50

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
			for new_genre in form.cleaned_data['genre']:
				print(new_genre)
				MovieGenres.objects.create(movie=new_movie, genre=new_genre,keyword=new_keyword)
				#MovieGenres.objects.create(movie=new_movie, keyword=new_keyword)
				
			return redirect(new_movie) # shortcut to object's get_absolute_url()
			# return HttpResponseRedirect(site.get_absolute_url())
		return render(request, 'movies/movie_new.html', {'form': form})

	def get(self, request):
		form = MovieForm()
		return render(request, 'movies/movie_new.html', {'form': form})	

		