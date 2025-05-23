from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'films', views.FilmViewSet)
router.register(r'critiques', views.CritiqueViewSet)
router.register(r'commentaires', views.CommentaireViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="MovieDB API",
        default_version='v1',
        description="API pour la plateforme de critique de films",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@moviedb.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    
    # Swagger documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]