#coding: utf8

import json
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

from skills.models import *
from skills.push import *

# REST API
def indexJSON(request):
	latest_skill_list = list(Skill.objects.order_by('pub_date')[:5])
	lista = map(lambda x: x.toDict(), latest_skill_list)
	response = HttpResponse(json.dumps(lista), content_type='application/json')
	response['Access-Control-Allow-Origin'] = '*'
	response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
	return response

def detailJSON(request, skill_id):
	skill = get_object_or_404(Skill, pk=skill_id)
	response = HttpResponse(skill.toJSON(), content_type='application/json')
	response['Access-Control-Allow-Origin'] = '*'
	response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
	return response

@csrf_exempt
def voteJSON(request, skill_id):
	if request.method == 'OPTIONS':
		response = HttpResponse('options ok')
		response['Access-Control-Allow-Origin'] = '*'
		response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
		response['Access-Control-Allow-Headers'] = 'Content-Type'
		return response

	p = get_object_or_404(Skill, pk=skill_id)
	try:
		selected_choice = p.choice_set.get(pk= json.loads(request.body)['choice'])
	except (KeyError, Choice.DoesNotExist):
		response = HttpResponse('error')
		response['Access-Control-Allow-Origin'] = '*'
		response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
		response['Access-Control-Allow-Headers'] = 'Content-Type'
		return response
	else:
		#if 'votes' in request.session:
		#	request.session['votes'].append(p.id)
		#else:
		#	request.session['votes'] = [p.id]

		selected_choice.votes += 1
		selected_choice.save()

		Push.Send("Nuevo voto en '" + p.skill_text + "'", {"skillid":p.id, "title":"+1 a '" + selected_choice.choice_text + "'"})


		response = HttpResponse('ok')
		response['Access-Control-Allow-Origin'] = '*'
		response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
		response['Access-Control-Allow-Headers'] = 'Content-Type'
		return response

@csrf_exempt
def registerDevice(request):
	if request.method == 'OPTIONS':
		response = HttpResponse('options ok')
		response['Access-Control-Allow-Origin'] = '*'
		response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
		response['Access-Control-Allow-Headers'] = 'Content-Type'
		return response

	if request.method == 'POST':
		data = json.loads(request.body)
		result = Push.Register(
			regid=data['regid'],
			uuid=data['uuid'],
			name=data['name'],
			platform=data['platform']
		)
		if result:
			response = HttpResponse('ok')
		else:
			response = HttpResponse('error')

		response['Access-Control-Allow-Origin'] = '*'
		response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
		response['Access-Control-Allow-Headers'] = 'Content-Type'
		return response

# Cliente Web
def index(request):
	latest_skill_list = Skill.objects.order_by('pub_date')[:5]
	context = {
		'latest_skill_list': latest_skill_list
	}
	return render(request, 'index.html', context)

def detail(request, skill_id):
	skill = get_object_or_404(Skill, pk=skill_id)
	return render(request, 'detail.html', {'skill':skill})

def results(request, skill_id):
	skill = get_object_or_404(Skill, pk=skill_id)
	return render(request, 'results.html', {'skill': skill})

def vote(request, skill_id):
	p = get_object_or_404(Skill, pk=skill_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render (request, 'detail.html', {
				'skill': p,
				'error_message': "No has seleccionado ninguna opción.",
			})
	else:
		if 'votes' in request.session:
			request.session['votes'].append(p.id)
		else:
			request.session['votes'] = [p.id]

		request.session.modified = True

		selected_choice.votes += 1
		selected_choice.save()

		Push.Send("Nuevo voto en '" + p.skill_text + "'", {"skillid":p.id, "title":"+1 a '" + selected_choice.choice_text + "'"})

		return HttpResponseRedirect(reverse('results', args=(p.id,)))