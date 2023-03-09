from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import UserViewSet


router = DefaultRouter()
router.register('users', UserViewSet)

app_name = 'api'

urlpatterns = [
    path('v1/', include(router.urls)),
]
