from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import UserViewSet, CategoriesViewSet, GenresViewSet, TitlesViewSet, ReviewViewSet, CommentViewSet


app_name = 'api'

v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')
v1_router.register('categories', CategoriesViewSet, basename='categories')
v1_router.register('generes', GenresViewSet, basename='generes')
v1_router.register('titles', TitlesViewSet, basename='titles')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
