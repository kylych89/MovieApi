from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from movieapp.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('api/v1/category', CategoryViewSet, basename='category')
router.register('api/v1/genre', GenreViewSet, basename='genre')
router.register('api/v1/user', UserViewSet, basename='user')
router.register('api/v1/movie', MovieViewSet, basename='movie')
router.register('api/v1/movie_shot', MovieShotsViewSet, basename='movie_shot')
router.register('api/v1/review', ReviewViewSet, basename='review')
router.register('api/v1/votes', VotesViewSet, basename='votes')



schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
# schema_view = get_schema_view(
#     openapi.Info(
#         title='Movie API',
#         default_version='v1',
#         description='Learn DRF',
#     ),
#     public=True,
#     permission_classes=(permissions.IsAuthenticated,)
# )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='swagger'),
]
urlpatterns += router.urls