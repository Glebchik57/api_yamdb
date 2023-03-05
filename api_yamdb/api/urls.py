from django.urls import path, include
# from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from api.views import UserViewSet


router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    # path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router.urls)),
]
