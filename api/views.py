from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import APIException
from django.core.cache import cache
from moviedb.models import Film, Critique, Commentaire
from accounts.models import CustomUser
from utils.myapi import TMDBServices
from .serializers import (
    CritiqueSerializer,
    CreateCritiqueSerializer,
    CommentaireSerializer,
    CreateCommentaireSerializer,
    FilmSerializer,
)
from django.db import models


# Pagination for FilmViewSet
class FilmPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 30


# Film ViewSet
class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = FilmPagination

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')

        if not query:
            return Response({"error": "Le paramètre 'q' est requis pour la recherche."}, status=400)

        cache_key = f"tmdb_search_{query}"
        cached_results = cache.get(cache_key)
        if cached_results:
            return Response(cached_results)

        try:
            tmdb_service = TMDBServices()
            results = tmdb_service.search_movies(query)
            # Cache the results for 1 hour
            cache.set(cache_key, results, timeout=3600)
            return Response(results)
        except Exception as e:
            raise APIException(f"Erreur lors de la recherche : {str(e)}")


# Critique ViewSet
class CritiqueViewSet(viewsets.ModelViewSet):
    queryset = Critique.objects.all()
    serializer_class = CritiqueSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        """Use different serializers for creation and retrieval."""
        if self.action in ['create', 'update', 'partial_update']:
            return CreateCritiqueSerializer
        return CritiqueSerializer

    def perform_create(self, serializer):
        """Automatically set the current user as the author of the critique."""
        serializer.save(utilisateur=self.request.user)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Retrieve all comments associated with a specific critique."""
        critique = self.get_object()
        comments = critique.commentaire_set.all()
        serializer = CommentaireSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Commentaire ViewSet
class CommentaireViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.all()
    serializer_class = CommentaireSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        """Use different serializers for creation and retrieval."""
        if self.action in ['create', 'update', 'partial_update']:
            return CreateCommentaireSerializer
        return CommentaireSerializer

    def perform_create(self, serializer):
        """Automatically set the current user as the author of the comment."""
        serializer.save(utilisateur=self.request.user)

def home(request):
    """Render the home page with featured content."""
    # Get featured movie (highest rated)
    featured_movie = Film.objects.order_by('-rating').first()
    
    # Get popular movies (top 4 by rating)
    popular_movies = Film.objects.order_by('-rating')[:4]
    
    # Get recent reviews (latest 4)
    recent_reviews = Critique.objects.select_related('user', 'movie').order_by('-created_at')[:4]
    
    # Get top contributors (users with most reviews)
    top_contributors = CustomUser.objects.annotate(
        review_count=models.Count('critique')
    ).order_by('-review_count')[:4]
    
    context = {
        'featured_movie': featured_movie,
        'popular_movies': popular_movies,
        'recent_reviews': recent_reviews,
        'top_contributors': top_contributors,
    }
    
    return render(request, 'home.html', context)