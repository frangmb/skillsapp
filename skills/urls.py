from django.conf.urls import patterns, url
from skills import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),

	# REST API
	url(r'^api/skills$', views.indexJSON, name="indexJSON"),
	url(r'^api/skills/(?P<skill_id>\d+)$', views.detailJSON, name='detailJSON'),
	url(r'^api/skills/(?P<skill_id>\d+)/vote$', views.voteJSON, name='voteJSON'),
	url(r'^api/register$', views.registerDevice, name='RegisterDevice_API'),
	
	# Cliente Web
	url(r'^(?P<skill_id>\d+)/$', views.detail, name='detail'),
	url(r'^(?P<skill_id>\d+)/results/$', views.results, name='results'),
	url(r'^(?P<skill_id>\d+)/vote/$', views.vote, name='vote'),
)