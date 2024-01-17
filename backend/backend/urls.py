"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from VetCalendar import views
import login.views as login_views
from django.conf import settings
from django.conf.urls.static import static
# from django.conf.urls import url
from django.views.generic.base import TemplateView
from login.views import validate_token

router = routers.DefaultRouter()
router.register(r'todos', views.TodoView, 'todo')
# router.register(r'upload_file', views.upload_file, 'upload')

urlpatterns = [
    path('', include('VetCalendar.urls')),
    re_path(r'admin\/?', admin.site.urls),
    re_path(r'api\/?', include(router.urls)),
    re_path(r'login\/?', include('login.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', validate_token, name='token_verify'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # cPanel

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # cPanel
