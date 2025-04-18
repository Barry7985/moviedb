from django.shortcuts import render , get_object_or_404 , redirect
from django.urls import reverse 
from django.core.paginator import Paginator
from itertools import chain
from django.views.generic import ListView , DetailView
from django.db.models import Q
from django.contrib import messages
from utils.myapi import TMDBServices
from .models import Film, Critique, Commentaire
from .forms import FilmFilterForm, SearchForm




class FilmListView(ListView):
    model = Film
    template_name = 'moviedb/list.html'
    context_object_name = 'films'
    paginate_by = 12

    def get_queryset(self):
        self.query = self.request.GET.get('query', '')
        local_results = Film.objects.filter(Q(titre__icontains=self.query) | Q(synopsis__icontains=self.query)) if self.query else Film.objects.all()
        tmdb_results = TMDBServices.search_movie(self.query).get('results', []) if self.query else []
        tmdb_films = [
            {
                'id': tmdb_result['id'],
                'titre': tmdb_result['title'],
                'synopsis': tmdb_result['overview'],
                'affiche': f"https://image.tmdb.org/t/p/w500{tmdb_result['poster_path']}" if tmdb_result['poster_path'] else None,
                'note_moyenne': tmdb_result['vote_average'],
                'duree': tmdb_result.get('runtime', 0),
                'date_sortie': tmdb_result['release_date'],
                'genres': [genre['name'] for genre in tmdb_result.get('genres', [])],
                'casting': '',
                'is_tmdb': True,
                'genre_list': [genre['name'] for genre in tmdb_result.get('genres', [])],
            }
            for tmdb_result in tmdb_results
        ]
        # Mark local results
        local_results = list(local_results)
        for film in local_results:
            film.is_tmdb = False
            # Add genre_list property for template compatibility
            film.genre_list = [g.strip() for g in film.genre.split(',')] if film.genre else []
        self.combined_results = list(chain(local_results, tmdb_films))
        paginator = Paginator(self.combined_results, self.paginate_by)
        page_number = self.request.GET.get('page')
        return paginator.get_page(page_number)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        films_page = self.get_queryset()
        context['films'] = films_page
        context['is_paginated'] = films_page.paginator.num_pages > 1 if hasattr(films_page, 'paginator') else False
        context['page_obj'] = films_page
        context['form'] = FilmFilterForm(self.request.GET or None)
        context['search_form'] = SearchForm(initial={'query': self.query})
        context['query'] = self.query
        context['total_results'] = len(self.combined_results)
        context['no_results'] = (self.query and context['total_results'] == 0)
        return context


class FilmDetailView(DetailView):
    model = Film
    template_name = 'moviedb/detail.html'
    context_object_name = 'film'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        film = self.get_object()
        critiques = film.critiques.select_related('utilisateur').prefetch_related('commentaires')
        context['critiques'] = critiques
        context['can_comment'] = self.request.user.is_authenticated
        context['comment_form'] = CommentaireForm() if self.request.user.is_authenticated else None
        context['login_url'] = reverse('accounts:login') if not self.request.user.is_authenticated else ''
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Vous devez être connecté pour commenter.")
            return redirect('accounts:login')
        self.object = self.get_object()
        film = self.object
        comment_form = CommentaireForm(request.POST)
        if comment_form.is_valid():
            commentaire = comment_form.save(commit=False)
            commentaire.utilisateur = request.user
            critique_id = request.POST.get('critique_id')
            commentaire.critique_id = critique_id
            commentaire.save()
            messages.success(request, "Commentaire ajouté avec succès.")
            return redirect('moviedb:film_detail', pk=film.pk)
        else:
            messages.error(request, "Erreur lors de l'ajout du commentaire. Veuillez vérifier le formulaire.")
        context = self.get_context_data()
        context['comment_form'] = comment_form
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('moviedb:film_detail', kwargs={'pk': self.object.pk})


def film_detail_tmdb(request, tmdb_id):
    # Récupére les détails du film depuis TMDB
    film_details = TMDBServices.get_movie_details(tmdb_id)
    
    if film_details:
        film = {
            'id': film_details['id'],
            'titre': film_details['title'],
            'synopsis': film_details['overview'],
            'affiche': f"https://image.tmdb.org/t/p/w500{film_details['poster_path']}" if film_details['poster_path'] else None,
            'note_moyenne': film_details['vote_average'],
            'duree': film_details.get('runtime', 0),
            'date_sortie': film_details['release_date'],
            'genres': [genre['name'] for genre in film_details.get('genres', [])],
            
        }
        return render(request, 'theater/film_detail_tmdb.html', {'film': film})
    else:
        messages.error(request, "Film non trouvé")
        return redirect('theater:film_list')