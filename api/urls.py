from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FilmViewSet, CritiqueViewSet, CommentaireViewSet

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'films', FilmViewSet, basename='film')  # Correctly includes the viewset
router.register(r'critiques', CritiqueViewSet, basename='critique')
router.register(r'commentaires', CommentaireViewSet, basename='commentaire')

urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)),
]