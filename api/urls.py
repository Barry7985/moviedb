from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FilmViewSet,
    CritiqueViewSet,
    CommentaireViewSet,
    home,
)

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'films', FilmViewSet, basename='film')  # Correctly includes the viewset
router.register(r'critiques', CritiqueViewSet, basename='critique')
router.register(r'commentaires', CommentaireViewSet, basename='commentaire')

urlpatterns = [
    # Home page
    path('', home, name='home'),
    # Include the router URLs
    path('api/', include(router.urls)),
]