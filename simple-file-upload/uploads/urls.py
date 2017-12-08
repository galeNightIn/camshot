from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from uploads.core import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^reg/', views.reg, name ='reg'),
    url(r'^admin/', admin.site.urls),
    url(r'^adobe_sample/', views.adobe_sample),
    url(r'^index/', views.index, name='index'),
    #name - name of html file
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
