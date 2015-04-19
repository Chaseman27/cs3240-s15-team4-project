from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project_prototype.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^SecureWitness/', include('SecureWitness.urls', namespace = 'SecureWitness')),
	url(r'^', include('SecureWitness.urls', namespace = 'SecureWitness'))
    
)
