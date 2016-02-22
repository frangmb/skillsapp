# coding:utf8
from django.conf import settings
from skills.models import *

def SiteInfo(request):
	return {
		'site_title': settings.SITE_TITLE,
		'site_subtitle': settings.SITE_SUBTITLE,
		'site_credits': settings.SITE_CREDITS,
	}

def LastActivity(request):
	result = {}
	if 'votes' in request.session:
		pks_list = request.session['votes']
		skills = list(Skill.objects.filter(pk__in=pks_list))
		skills.sort(key=lambda t: pks_list.index(t.pk))
		result['last_skills'] = skills

	return result