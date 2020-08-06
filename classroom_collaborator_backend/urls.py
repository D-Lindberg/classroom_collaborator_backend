"""classroom_collaborator_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.schemas import get_schema_view




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Classroom.urls')),
    # path('token-auth/', obtain_jwt_token),
    path('auth/', include('rest_framework.urls')),
    
    # api end point visual test
    path('openapi', get_schema_view(
        title='classhub',
        description="outline what endpoints are available",
        version="1.0.0"
    ), name='openapi-schema'),


]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
