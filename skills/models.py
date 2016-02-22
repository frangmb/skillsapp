# coding:utf8

from __future__ import unicode_literals

import json
from django.db import models

# Create your models here.
class Skill(models.Model):
	skill_text = models.CharField(max_length=200)
	icon = models.CharField(max_length=50)
	pub_date = models.DateTimeField('date published')

	def __str__(self):
		return self.skill_text.encode('utf-8')

	def toDict(self):
		votesList = []
		for c in self.choice_set.all():
			votesList.append({'name': c.choice_text, 'votes': c.votes, 'id': c.pk})

		return {
			'id': self.id,
			'name': self.skill_text,
			'icon': self.icon,
			'pub_date': self.pub_date.strftime("%Y-%m-%d %H:%M:%S"), #AAAA-MM-DD HH:MM:SS
			'options': votesList
		}

	def toJSON(self):
		return json.dumps(self.toDict())

class Choice(models.Model):
	skill = models.ForeignKey(Skill)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return self.choice_text.encode('utf-8')