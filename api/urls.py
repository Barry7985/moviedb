from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import FilmViewSet, CritiqueViewSet, CommentaireViewSet

app_name = 'api'
# Create a router and register the viewsets
router = SimpleRouter
router.register(r'films', FilmViewSet, basename='film')
router.register(r'critiques', CritiqueViewSet, basename='critique')
router.register(r'commentaires', CommentaireViewSet, basename='commentaire')

urlpatterns = router.urls