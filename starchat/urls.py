"""
URL configuration for starchat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from starchat.views import CurrentUserView, CommentViewSet
from starchat.views import PostViewSet
from starchat.views.auto_response import AutoResponseViewSet
from starchat.views.comment_analytics import CommentAnalyticsView

api_urlpatterns = [
    # path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('rest_registration.api.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('user/current/', CurrentUserView.as_view()),
    path('post/', PostViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('post/<id>/', PostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('comment/', CommentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('comment/<id>/', CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('analytics/comments/', CommentAnalyticsView.as_view()),
    path('auto_response/', AutoResponseViewSet.as_view({'get': 'retrieve', 'post': 'create'})),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_urlpatterns)),
]
