from django.urls import path
from . import views

app_name = 'moviedb'  # Namespace for the app

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # Film list view (class-based view)
    path('films/', views.FilmListView.as_view(), name='film_list'),

    # Film detail view for local films (class-based view)
    path('films/<int:pk>/', views.FilmDetailView.as_view(), name='film_detail'),

    # Film detail view for TMDB films (function-based view)
    path('films/tmdb/<int:tmdb_id>/', views.film_detail_tmdb, name='film_detail_tmdb'),
]