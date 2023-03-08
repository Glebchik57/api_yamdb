from django.urls import path, include
# from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from api.views import UserViewSet, get_token, sign_up


router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', sign_up),
    path('v1/auth/token/', get_token),
]
