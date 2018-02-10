"""proj2004 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.views import static
from django.urls import path, include

urlpatterns = [
    path('account/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', include('contacts.urls')),
]

if settings.DEBUG:
    # Serve uploaded files for development mode
    urlpatterns.append(path(settings.MEDIA_URL[1:] + '<path:path>',
        static.serve, {'document_root': settings.MEDIA_ROOT}))
    # For debug toolbar
    import debug_toolbar
    urlpatterns.insert(0, path('__debug__/', include(debug_toolbar.urls)))
