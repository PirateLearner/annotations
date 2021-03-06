from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^annotations/', include('annotations.urls', namespace='annotations')),
    url(r'^blogging/', include('blogging.urls',namespace='blogging')),
    url(r'^$', 'demo.views.home', name='home'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
